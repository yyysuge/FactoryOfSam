#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class ProductInfo:

    def __init__(self,product_name):
        # self.browser = webdriver.PhantomJS()
        # self.browser.set_window_size(1366, 768)
        self.browseroption = webdriver.ChromeOptions()
        self.browseroption.add_argument('headless')
        self.browseroption.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.browseroption)
        self.product_name = product_name

    def crawlproduct(self):
        self.browser.get("http://www.taobao.com")
        try:
            wait = WebDriverWait(self.browser, 10)
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#q")))
            button = self.browser.find_element_by_css_selector("#J_TSearchForm > div.search-button > button")
            input.clear()
            input.send_keys(self.product_name)
            button.send_keys(Keys.ENTER)
            time.sleep(3)
            self.getonepageproductinfo()
            pagenum = 1
            while pagenum < 3:
                pagenum = pagenum + 1
                print pagenum
                input_page = self.browser.find_element_by_css_selector("#mainsrp-pager > div > div > div > div.form > input")
                button_page = self.browser.find_element_by_css_selector("#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")
                input_page.clear()
                input_page.send_keys(str(pagenum))
                button_page.send_keys(Keys.ENTER)
                time.sleep(3)
                self.getonepageproductinfo()

        finally:
            pass
            #self.browser.quit()

    def getonepageproductinfo(self):
        print self.browser.current_url
        index = 1
        while index <= 44:
            try:
                product_item = self.browser.find_element_by_css_selector("#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child("+ str(index) +")> div.ctx-box.J_MouseEneterLeave.J_IconMoreNew ")
                product_name = product_item.find_element_by_css_selector("div.row.row-2.title").text
                product_price = product_item.find_element_by_css_selector("div.row.row-1.g-clearfix > div.price.g_price.g_price-highlight > strong").text
                product_sales = product_item.find_element_by_css_selector("div.row.row-1.g-clearfix > div.deal-cnt").text
                product_producer = product_item.find_element_by_css_selector("div.row.row-3.g-clearfix > div.shop").text
                product_palce = product_item.find_element_by_css_selector("div.row.row-3.g-clearfix > div.location").text
                product_href = product_item.find_element_by_css_selector("div.row.row-2.title").find_element_by_class_name("J_ClickStat").get_attribute("href")
                print index,product_name, product_price, product_sales, product_producer, product_palce, product_href
                index += 1
            except NoSuchElementException,e:
                print e
                index2 = 1
                while index2 <= 12:
                    try:
                        product_item = self.browser.find_element_by_css_selector("#J_itemlistPersonality > div > div:nth-child("+str(index2)+") > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew")
                        product_name = product_item.find_element_by_css_selector("div.row.row-2.title").text
                        product_price = product_item.find_element_by_css_selector("div.row.row-1.g-clearfix > div.price.g_price.g_price-highlight > strong").text
                        product_sales = product_item.find_element_by_css_selector("div.row.row-1.g-clearfix > div.deal-cnt").text
                        product_producer = product_item.find_element_by_css_selector("div.row.row-3.g-clearfix > div.shop").text
                        product_palce = product_item.find_element_by_css_selector("div.row.row-3.g-clearfix > div.location").text
                        product_href = product_item.find_element_by_css_selector("div.row.row-2.title").find_element_by_class_name("J_ClickStat").get_attribute("href")
                        print index2, product_name, product_price, product_sales, product_producer, product_palce, product_href
                        index2 += 1
                    except NoSuchElementException,e:
                        print e.message
                        break
                break

    def __del__(self):
        #self.browser.close()
        print "del"


if __name__ == "__main__":
    sonyinf = ProductInfo(u"斗柜")
    sonyinf.crawlproduct()
