# 安装
```bash
pip install -r requirements.txt
```
# 说明
爬虫示例文件见`spider/main.py.`

`spider`文件夹主要用于爬取信息、得到监督数据。`spider.bilibili_spider.BilibiliSpider`用于从B站爬取视频以及弹幕数据。
```python
def get_danmaku(self, bv_id: str, xml_path: str) -> None:
    """
    将指定BV号的弹幕保存为xml文件。
    :param bv_id: BV号
    :param xml_path: xml文档保存路径
    """
    pass

def get_video(self, bv_id: str, video_path: str) -> None:
    """
    将指定BV号的弹幕保存为视频文件。由于B站视频和音频不是一起存的，所以视频只有画面没有声音。
    :param bv_id: BV号
    :param video_path: 视频保存路径
    """
    pass
```
`spider.utils.VideoProcessor`用于从视频中提取监督信息，从而进行后续训练。有三个方法是核心(TODO)：
```python
def _get_danmaku_score(self, danmakus: List[str]) -> float:
    """
    给定弹幕列表，返回该弹幕的(情感)得分。该得分会作为该帧的监督信号。
    :param danmakus: List[str], 弹幕列表
    :return: 弹幕情感得分score, 0 <= score <= 1
    """
    # TODO

def _is_interested_frame(self, frame: np.ndarray) -> bool:
    """
    给定帧，确定该帧是否包含感兴趣内容(比如检测到猫)。只有感兴趣内容才会被进一步处理(如提取关节)。
    :param frame: np.ndarray(h, w), uint8表示的帧
    :return: bool, 该帧是否包含感兴趣内容
    """
    # TODO

def _get_feature(self, frame: np.ndarray) -> np.ndarray:
    """
    给定帧，从该帧中提取关节特征信息。
    :param frame: np.array(h, w), uint8表示的帧
    :return: np.array, 从该帧中提取得到的关节信息，用于构建数据集进行训练。
    """
    # TODO
```
实现以上三个方法之后，可以调用`VideoProcessor.process`获取标注数据对。
```python
 def process(self, video_path: str, xml_path: str) -> None:
    """
    :param video_path: 视频路径
    :param xml_path: 弹幕路径
    """
    pass
```