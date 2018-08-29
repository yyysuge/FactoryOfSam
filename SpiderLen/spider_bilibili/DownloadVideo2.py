# encoding: utf-8
"""
date:20180715
function:解析B站视频播放流程，下载B站视频，抓包分析发现不需要sign参数了
"""
import urllib2
import ssl
import json
import zlib
from pyquery import PyQuery as pq
import re

ssl._create_default_https_context = ssl._create_unverified_context

class GetBiVideo:
    def __init__(self, id=""):
        self.video_id = id
        self.video_url = "https://www.bilibili.com/video/" + self.video_id
        self.video_heaeders = {
            'Host': ' www.bilibili.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': ' 1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.bilibili.com/video/av21701018?spm_id_from=333.338.__bofqi.11',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': ' zh-CN,zh;q=0.9',
        }
        self.video_cid = ""
        self.video_name = ""
        self.info_url = ""
        self.info_headers = {
            'Host': ' interface.bilibili.com',
            'Connection': ' keep-alive',
            'Accept': ' application/json, text/javascript, */*; q=0.01',
            'Origin': ' https://www.bilibili.com',
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': ' https://www.bilibili.com/video/av16188109?p=3',
            # 'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': ' zh-CN,zh;q=0.9'
        }

        self.dl_url = ""
        self.dl_headers = {
            'Host': 'upos-hz-mirrorks3.acgvideo.com',
            'Connection': 'keep-alive',
            'Origin': ' https://www.bilibili.com',
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': ' */*',
            'Referer': 'https://www.bilibili.com/video/'+self.video_id,
            'Accept-Encoding': '  gzip, deflate, br',
            'Accept-Language': ' zh-CN,zh;q=0.9',
            'Range': ' bytes=0-'
        }

    def getupmasterinfo(self):

        #step1:from videohtml get cid
        request_html = urllib2.Request(url=self.video_url,headers=self.video_heaeders)
        response_html = urllib2.urlopen(request_html)
        response_str = response_html.read()
        gzipped = response_html.headers.get('Content-Encoding')
        if gzipped:
            response_str = zlib.decompress(response_str, 16 + zlib.MAX_WBITS)
        #print response_str.decode("utf-8")
        doc_info = pq(response_str.decode("utf-8"))

        self.video_name = doc_info("title").text()
        self.video_name = self.video_name.replace("/","")
        self.video_name = self.video_name.replace("\\", "")
        self.video_name = self.video_name + ".flv"
        print "download:" + self.video_name
        json_info = doc_info.items("script")

        for item in json_info:
            result = re.search(r'window.__playinfo__={(.*)}', item.text())

            if result:
                t_dict = result.group(1)
                print t_dict

        #         self.info_url = "https://interface.bilibili.com/v2/playurl?cid=" + self.video_cid + "&appkey=84956560bc028eb7&otype=json&type=&quality=64&qn=64&sign=d141e08092dc06076f13f1fe2bbe95d5"
        # print self.info_url
        # #step2:from api get dl_url
        # request_info = urllib2.Request(url=self.info_url, headers=self.info_headers)
        # response_info = urllib2.urlopen(request_info)
        # json_info = json.loads(response_info.read())
        # self.dl_url = json_info["durl"][0]["url"]
        # #step3:download video by dl_url
        # request_video = urllib2.Request(url=self.dl_url, headers=self.dl_headers)
        # response_video = urllib2.urlopen(request_video)
        #
        # with open(self.video_name , "wb") as f:
        #     f.write(response_video.read())

        # html = etree.HTML(response_html)
        # html = html.xpath("//script@type=application/ld+json")
        # #result = etree.tostring(html)
        # print html


if __name__ == "__main__":
    pp = GetBiVideo("av3236596")
    pp.getupmasterinfo()
