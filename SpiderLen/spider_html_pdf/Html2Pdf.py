#coding=utf-8

import os
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pdfkit
import requests
from lxml import etree
import pprint
from pyquery import PyQuery as pq
from PyPDF2 import PdfFileReader, PdfFileWriter
from time import time

"""
total time: 107.98300004
"""

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

class Html2PDF(object):
    def __init__(self,url):
        self.__url = url

    def get_url_list(self):
        headers = {
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"""
        }
        try:
            response = requests.get(url=self.__url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                html = response.text
                url_list = []
                """
                Beautiful Soup库
                """
                """
                soup = BeautifulSoup(html,'html.parser')
                #print soup.prettify()
                ul = soup.find_all("ul",attrs={"class":"pagemenu"})#find_all方法的返回值是一个列表
                li_list = ul[0].find_all("li")
                for li in li_list:
                    try:
                        #print li.string," : ",li.a["href"]
                        url_list.append({"title":li.string,"url":li.a["href"]})
                    except KeyError,e:#获取不到属性，抛出KeyError
                        url_list.append({"title":li.string,"url":""})
                        print "KeyError:",e
                return url_list
                """

                """
                lxml库，XPath语法
                """
                """
                page = etree.HTML(html)
                li_list = page.xpath("//ul[@class='pagemenu']/li")
                for li in li_list:
                    url_list.append({"title": li[0].text, "url": li[0].get("href")})
                return url_list
                """

                """
                PyQuery库
                """
                page = pq(html)
                items = page('.pagemenu li').children()#结果是lxml.html.HtmlElement类型
                for item in items:
                    url_list.append({"title": item.text, "url": item.get("href")})
                return url_list

            return None
        except RequestException as e:
            print "except:",e
            return None

    def __get_one_page_html(self,url):
        """
        获取网页html内容并返回
        :param
        :return html
        """
        headers = {
            'User-Agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"""
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            return None
        except RequestException as e:
            print "except:", e
            return None

    def __get_html_content(self,url):
        """
        解析URL，获取需要的html内容
        :param url: 目标网址
        :return: html
        """
        html = self.__get_one_page_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', attrs={'class': 'article-content'})
        html = html_template.format(content=content)
        return html.decode("utf-8")

    def __get_one_pdf(self,url, title):
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
            html = self.__get_html_content(url)
            pdfkit.from_string(html, title.replace("/", "") + ".pdf")
        except Exception as e:
            print "except:", e

    def get_full_pdf(self,url_list):

        for item in url_list:
            if item["title"] == None:
                self.__get_one_pdf(self.__url, u"MongoDB教程")
            if item["url"] != None and item["title"] != None:
                self.__get_one_pdf(item["url"], item["title"])
        pdf_output = PdfFileWriter()
        try:
            for item in url_list:
                if item["url"] != None:
                    if item["title"] == None:
                        pdf_input = PdfFileReader(open(u"MongoDB教程.pdf", 'rb'))
                        page_count = pdf_input.getNumPages()
                        for i in range(page_count):
                                pdf_output.addPage(pdf_input.getPage(i))
                    else:
                        pdf_input = PdfFileReader(open(item["title"].replace("/","")+".pdf", 'rb'))
                        page_count = pdf_input.getNumPages()
                        for i in range(page_count):
                            pdf_output.addPage(pdf_input.getPage(i))
            pdf_output.write(open(u"MongoDB教程_full.pdf", 'wb'))
        except IOError,e:
            print "except:",e

    def del_file(self,url_list):
        try:
            for item in url_list:
                if item["url"] != None:
                    if item["title"] == None:
                        os.remove(u"MongoDB教程.pdf")
                    else:
                        os.remove(item["title"].replace("/","")+".pdf")
        except WindowsError,e:
            print "except:",e


def main():
    starttime = time()
    print "start time:",starttime
    url = "https://www.yiibai.com/mongodb/"
    pp = Html2PDF(url)
    url_list = pp.get_url_list()
    pp.get_full_pdf(url_list)
    endtime = time()
    print "end time:",endtime
    print "total time:",endtime - starttime
    #pp.del_file(url_list)

if __name__ == "__main__":
    main()