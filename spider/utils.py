import cv2
import numpy as np
from typing import List, Tuple
import xml.etree.ElementTree as ET

def get_time_from_attr(attributes: str) -> float:
    """
    从p属性获取该弹幕于视频的开始时间。
    :param attributes: 从parse中获取的p属性attribute字符串
    :return: 返回该弹幕的开始时间(s)。
    """
    attrs = attributes.split(',')
    start_time = attrs[0]
    return float(start_time)

def parse_xml(xml_path: str, sort=True) -> List[Tuple[float, str]]:
    """
    将指定xml文件转为表示弹幕的列表。列表的每个元素是一个二元组(start_time: float, text: str),
    分别表示开始时间(秒)和文本。
    :param xml_path: xml文档路径
    :param sort: 是否按时间排序
    :return: List[Tuple[float, str]], 如上文所述
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    result = []
    for child in root:
        if 'p' in child.attrib:
            attributes = child.get('p')
            text = child.text
            result.append((get_time_from_attr(attributes), text))
    if sort:
        result.sort()
    return result

class VideoProcessor:
    """
    该类用于从视频中提取监督信息，用于后续训练。
    """
    def __init__(self, scoring_threshold=5):
        """
        :param scoring_threshold: 只有某帧附近的弹幕数 > scoring_threshold 才会被考虑
        """
        self.current_ptr = 0
        self.scoring_threshold = scoring_threshold
    
    def _get_neighbor_danmaku(self, danmaku: List[Tuple[float, str]], time_stamp: float, k_neighbor=10) -> List[str]:
        """
        从弹幕列表中找出附近的弹幕。选取规则: 选取弹幕发送时间 >= time_stamp 的至多k_neighbor条弹幕。
        :param danmaku: parse_xml返回的弹幕列表, **需要按照时间排序。**
        :param time_stamp: 指定的时间戳
        :param k_neighbor: 至多选取多少条弹幕
        :return: List[str], 选取的弹幕列表
        """
        while self.current_ptr < len(danmaku) and danmaku[self.current_ptr][0] < time_stamp:
            self.current_ptr += 1
        tuples = danmaku[self.current_ptr: self.current_ptr+k_neighbor]
        danmakus = [item[1] for item in tuples]
        return danmakus

    def _get_danmaku_score(self, danmakus: List[str]) -> float:
        """
        给定弹幕列表，返回该弹幕的(情感)得分。该得分会作为该帧的监督信号。
        :param danmakus: List[str], 弹幕列表
        :return: 弹幕情感得分score, 0 <= score <= 1
        """
        # TODO
        return 1.0

    def _is_interested_frame(self, frame: np.ndarray) -> bool:
        """
        给定帧，确定该帧是否包含感兴趣内容(比如检测到猫)。只有感兴趣内容才会被进一步处理(如提取关节)。
        :param frame: np.ndarray(h, w), uint8表示的帧
        :return: bool, 该帧是否包含感兴趣内容
        """
        # TODO
        return True
    
    def _get_feature(self, frame: np.ndarray) -> np.ndarray:
        """
        给定帧，从该帧中提取关节特征信息。
        :param frame: np.array(h, w), uint8表示的帧
        :return: np.array, 从该帧中提取得到的关节信息，用于构建数据集进行训练。
        """
        # TODO
        return frame.sum(0)

    def process(self, video_path: str, xml_path: str) -> List[Tuple[np.ndarray, float]]:
        """
        :param video_path: 视频路径
        :param xml_path: 弹幕路径
        :return: List[Tuple[np.ndarray, float]], 提取得到的监督数据
        """
        cap = cv2.VideoCapture(video_path)
        danmaku = parse_xml(xml_path, sort=True)
        self.current_ptr = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            time_stamp = cap.get(cv2.CAP_PROP_POS_MSEC) # 该帧的时间戳(ms)
            time_stamp /= 1000 # ms -> s

            current_danmaku = self._get_neighbor_danmaku(danmaku, time_stamp)

            if len(current_danmaku) > self.scoring_threshold: # 弹幕数量足够多
                if self._is_interested_frame(frame): # 该帧为感兴趣帧(比如包含猫的图像)
                    danmaku_score = self._get_danmaku_score(current_danmaku)
                    features = self._get_feature(frame)
          
                    # (features, danmaku_score) 为一组数据, 0 <= danmaku_score <= 1是监督信号

if __name__ == '__main__':
    processor = VideoProcessor()
    processor.process('data/video/1.mp4', 'data/xml/1.xml')