# coding=utf-8
import urllib2
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context


class GetBiVideo:
    def __init__(self):
        self.url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=35850273&pagesize=30&tid=0&page=1&keyword=&order=pubdate"
        self.headers = {
            "Host": "space.bilibili.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "Referer": " https://space.bilibili.com/35850273/",
            # "Accept-Encoding": " gzip, deflate, br",
            "Accept-Language": " zh-CN,zh;q=0.9"
        }
        self.num = 0

    def getupmasterinfo(self):
        request = urllib2.Request(url=self.url, headers=self.headers)
        response = urllib2.urlopen(request)
        videolist = json.loads(response.read().decode("utf-8"))
        print videolist['data']


if __name__ == "__main__":
    pp = GetBiVideo()
    pp.getupmasterinfo()
