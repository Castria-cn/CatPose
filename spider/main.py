from bilibili_spider import BilibiliSpider
from utils import parse_xml

if __name__ == '__main__':
    spider = BilibiliSpider()
    spider.get_danmaku('BV1Bw411H7un', './data/1.xml')
    parse_result = parse_xml('./data/1.xml', sort=True)
    print(parse_result[0])