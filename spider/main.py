from bilibili_spider import BilibiliSpider
from utils import parse_xml, VideoProcessor

if __name__ == '__main__':
    spider = BilibiliSpider()

    spider.get_danmaku('BV1Bw411H7un', 'data/xml/1.xml') # 获取弹幕文件并保存至data/xml/1.xml
    spider.get_video('BV1Bw411H7un', 'data/video/1.mp4') # 获取视频文件并保存至data/video/1.mp4

    processor = VideoProcessor('./data/train.csv')
    processor.process('./data/video/1.mp4', './data/xml/1.xml') # 从视频中提取数据并追加到data/train.csv中