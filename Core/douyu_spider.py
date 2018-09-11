# coding=utf-8
from selenium import webdriver
import time
from lxml import etree
import json

class DouyuSpider:

    def __init__(self):
        # 创建无头浏览器对象
        self.driver = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # 当前页码数
        self.cur_page = 1


    # 点击下一页
    def click_next_page(self):
        self.driver.get(self.start_url)
        html_str = self.driver.page_source
        print(html_str)
        print("*"*100)


        #获取下一页的元素
        next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
        next_url = next_url[0] if len(next_url)>0 else None
        next_url.click()
        html_str = self.driver.page_source
        print(html_str)

        print("*" * 100)
        #获取下一页的元素
        next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
        next_url = next_url[0] if len(next_url)>0 else None
        next_url.click()
        html_str = self.driver.page_source
        print(html_str)



    def get_html_str(self):
        self.driver.get(self.start_url)
        html_str = self.driver.page_source
        return html_str


    # 获取所有的item对象
    def get_item_list(self , html_str):

        # html字符串转换为Element对象
        html = etree.HTML(html_str)

        # 获取所有的li块
        li_list = html.xpath("//ul[@id='live-list-contentbox']/li")
        # 存放item对象的列表
        item_list = []
        # 提取每一个li块为item对象
        for li in li_list:
            # item对象
            item = {}
            item["room_img"]=li.xpath(".//span[@class='imgbox']/img/@src")
            item["room_title"] = li.xpath("./a/@title")
            item["room_cate"] = li.xpath(".//span[@class='tag ellipsis']/text()")
            item["anchor_name"] = li.xpath(".//span[@class='dy-name ellipsis fl']/text()")
            item["watch_num"] = li.xpath(".//span[@class='dy-num fr']/text()")
            # print(item)
            item_list.append(item)

        # 获取下一页的元素
        next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")
        # next_url = html_str.xpath("//a[@class='shark-pager-next']")
        # 判断是否获取到下一页元素
        next_url = next_url[0] if len(next_url) > 0 else None
        # print(next_url)
        return item_list , next_url


    # 保存item_list对象
    def save_item_list(self , item_list , file_path):
        # 文件的路径
        file_path = file_path

        # 打开文件 , 写入数据
        with open(file_path , "a" , encoding="utf-8") as f:
            for item in item_list:
                # python类型转json字符串 , 写入文件 , indent表示缩进
                f.write(json.dumps(item , ensure_ascii=False , indent=2))
                # 写入换行
                f.write("\n")
        print("保存成功")


    # 实现主要逻辑
    def run(self):

        html_str = self.get_html_str()
        # 获取一页的item_list对象与下一页的url
        item_list , next_url = self.get_item_list(html_str)
        # 保存item_list数据
        self.save_item_list(item_list , "斗鱼二次元信息.txt")
        print("第"+str(self.cur_page)+"页数据爬取成功")
        self.cur_page += 1

        # 点击下一页 , 获取下一页的item_list
        while next_url is not None:
            # 点击了下一页 , html源码已经改变了
            next_url.click()
            # 更新html源码
            html_str = self.driver.page_source
            time.sleep(3)
            item_list , next_url = self.get_item_list(html_str)
            print(item_list)
            # self.save_item_list(item_list , "斗鱼二次元信息.txt")


        # # 发送请求
        # self.driver.get(self.start_url)
        # # 提取item_list数据
        # item_list , next_url = self.get_item_list()
        # # 保存数据
        # self.save_item_list()
        # # 点击下一页 , 获取下一页的item_list
        # while next_url is not None:
        #     next_url.click()
        #     time.sleep(3)
        #     item_list , next_url = self.get_item_list()
        #     self.save_item_list()



if __name__ == '__main__':
    douyu = DouyuSpider()
    # 爬取数据的起始地址
    douyu.start_url = "https://www.douyu.com/g_ecy"
    douyu.click_next_page()
    # douyu.run()
