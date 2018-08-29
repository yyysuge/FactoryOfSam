#coding=utf-8
import os
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pdfkit
import requests

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

class OnePageHtml2PDF():
    def __init__(self,url):
        self.__url = url

    def get_one_page_html(self):
        """
        获取网页html内容并返回
        :param
        :return html
        """
        headers = {
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"""
        }

        try:
            response = requests.get(self.__url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            return None
        except RequestException as e:
            return None

    def get_content(self):
        """
        解析URL，获取需要的html内容
        :param url: 目标网址
        :return: html
        """
        html = self.get_one_page_html()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', attrs={'class': 'article-content'})
        html = html_template.format(content=content)
        return html.decode("utf-8")

    def get_pdf(self):
        """
        解析URL，获取html，保存成pdf文件
        :return: None
        """
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        try:
            html = self.get_content()
            title = u"MongoDB安装配置(RedHat/CentOS).pdf"
            title = title.replace("/","")
            print title
            print type(title)
            #pdfkit.from_string(html, title)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    pp = OnePageHtml2PDF("https://www.yiibai.com/mongodb/install-mongodb-on-redhat.html")
    pp.get_pdf()