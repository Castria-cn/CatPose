import numpy as np
from mmpose.apis import MMPoseInferencer

class MMPoseWrapper:
    def __init__(self):
        self.inferencer = MMPoseInferencer('animal')
    def inference(self, image: np.ndarray, show=False) -> dict:
        """
        :param image: np.ndarray, 输入图像
        :return: 推理结果 json,
        pred_i = json['predictions'][0][i] 为第 i 个预测，
        pred_i['keypoints']: List[List[float]], (17, 2), 每行是一个关键点
        pred_i['keypoint_scores']: List[float], (17,), 每行是一个关键点得分
        pred_i['bbox'][0]: (4, ), bbox
        pred_i['bbox_score']: float, bbox置信度
        """
        result = self.inferencer(image, show=show)
        return next(result)