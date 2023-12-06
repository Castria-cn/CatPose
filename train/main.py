import cv2
import yaml
import torch
import numpy as np
from torch import nn
from tqdm import tqdm
from typing import Union
from torch.utils.data import DataLoader
from network import PoseNet, KeyPointDataset
from inf_utils import VideoProcessor

class PoseScoreWrapper:
    def __init__(self, cfg_path: str, model=None):
        """
        :param cfg_path: yaml配置文件路径
        :param model: 模型文件路径, 默认为随机初始化
        """
        with open(cfg_path, 'r', encoding='utf-8') as yaml_file:
            self.cfg = yaml.safe_load(yaml_file)
        if model:
            self.model = torch.load(model)
        else:
            self.model = PoseNet()
        
        if torch.cuda.is_available():
            self.model.to('cuda')

    def train(self) -> None:
        """
        使用关键点信息进行模型训练。
        """
        dataset = KeyPointDataset(self.cfg['csv_path'])
        loader = DataLoader(dataset, batch_size=self.cfg['batch_size'])

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.cfg['lr'])
        if self.cfg['criteriono'] == 'MSE':
            criterion = nn.MSELoss()

        self.model.train()
        for i in range(self.cfg['epoch']):
            for X, y in tqdm(loader, desc=f'Training epoch {i + 1}'):
                if torch.cuda.is_available():
                    X = X.to('cuda')
                    y = y.to('cuda')
                y = y.reshape(-1, 1)
                
                pred_y = self.model(X)
                loss = criterion(pred_y, y)

                loss.backward()
                optimizer.zero_grad()
                optimizer.step()
            
            if i % self.cfg['save_epoch'] == self.cfg['save_epoch'] - 1:
                torch.save(self.model, self.cfg['model_path'] + f'/model_epoch{i + 1}.pt')
        
        torch.save(self.model, self.cfg['model_path'] + f'/model_final.pt')
    
    def inference(self, img: Union[str, np.ndarray]) -> float:
        """
        使用模型推理得分。
        :param img_path: 图片文件路径 / numpy多维数组(h, w, c)
        :return: 推理得分 0 <= score <= 1
        """
        if not hasattr(self, 'processor'):
            self.processor = VideoProcessor(self.cfg['csv_path'])
        
        if type(img) == str:
            frame = cv2.imread(img)
        interested, result = self.processor.is_interested_frame(frame)

        if not interested: # 不含猫
            return 0.

        cat_id = [key for key, value in result['name'].items() if value == 'cat'][0]
        x_min, y_min = int(result['xmin'][cat_id]), int(result['ymin'][cat_id])
        x_max, y_max = int(result['xmax'][cat_id]), int(result['ymax'][cat_id])
        roi = frame[y_min:y_max, x_min:x_max,:]

        flag, features = self.processor.get_feature(roi)

        if not flag: # 无法获取关节点
            return 0.
        
        features = torch.from_numpy(features).reshape(1, -1).to(torch.float)
        self.model.eval()
        
        pred_score = self.model(features)
        return float(pred_score)
        

if __name__ == '__main__':
    wrapper = PoseScoreWrapper('config/train.yaml')
    inf_result = wrapper.inference('demo/demo.jpeg')
    print(f'图片得分: {inf_result}')

        