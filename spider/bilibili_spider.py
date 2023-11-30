import requests

class BilibiliSpider:
    def __init__(self):
        pass
    def get_cid(self, bv_id: str) -> str:
        """
        B站视频内部用cid表示，获取弹幕需要从BV号转cid.
        :param bv_id: 视频BV号
        :return: 视频的cid
        """
        url = f'https://api.bilibili.com/x/player/pagelist?bvid={bv_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        req = requests.get(url, headers=headers)
        result = req.json()
        assert 'data' in result # result['data'][0]['cid']

        return result['data'][0]['cid']
    def get_danmaku(self, bv_id: str, xml_path: str) -> None:
        """
        将指定BV号的弹幕保存为xml文件。
        :param bv_id: BV号
        :param xml_path: xml文档保存路径
        """
        cid = self.get_cid(bv_id)
        danmaku_url = f'https://comment.bilibili.com/{cid}.xml'
        req = requests.get(danmaku_url)
        req.encoding = 'utf-8'
        if req.status_code == 200:
            with open(xml_path, 'wb') as file:
                file.write(req.content)
                file.close()