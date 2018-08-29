#coding=utf-8
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapylen1.items import Scrapylen1Item


class Myspider(scrapy.Spider):
    name = 'scrapylen1'
    allowed_domains = ['qidian.com']
    max_page_num = 0
    page_num = 1
    start_urls=["https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page="+str(page_num)]

    def parse(self, response):
        soup = BeautifulSoup(response.text)
        if self.page_num == 1:
            result = soup.find_all(name = "a",attrs={"class":"lbf-pagination-page "})
            self.max_page_num = int(result[-1].string)
        if self.page_num<= self.max_page_num:
            item = Scrapylen1Item()
            books = soup.find_all(name = "div",attrs={"class":"book-mid-info"})
            for book in books:
                item["name"] = book.h4.a.string
                item["author"] = book.p.a.string
                item["novelurl"] = book.h4.a["href"]
                item["serialstatus"] = book.p.span.string
                item["category"] = book.p.find_all(name = "a")[1].string+"_"+book.p.find_all(name = "a")[2].string
                item["name_id"] = book.h4.a["data-bid"]
                yield item

