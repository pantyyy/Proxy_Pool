#coding:utf-8

import requests
from lxml import etree
import json
import random
import time

class ProxyIPPool:
    # 初始化
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    # 获取目标页面源码(二进制)
    def get_html_source(self , url):
        print(url)
        # 发送请求获取响应
        response = requests.get(url , headers=self.headers)
        return response.content

    # 提取数据为对象列表
    def get_item_list(self , html_str):
        # 解析html
        html = etree.HTML(html_str)

        # 根据tr进行分组
        tr_list = html.xpath('//table[@class="table table-bordered table-striped"]/tbody//tr')

        # 存放对象的列表
        item_list = []

        # 循环 , 提取item对象
        for tr in tr_list:
            item = {}
            item["ip"] = tr.xpath("./td[position()=1]/text()")[0] if len(tr.xpath("./td[position()=1]/text()")) > 0 else None
            item["socket"] = tr.xpath("./td[position()=2]/text()")[0] if len(tr.xpath("./td[position()=2]/text()")) > 0 else None
            item["location"] = tr.xpath("./td[position()=6]/text()")[0] if len(tr.xpath("./td[position()=6]/text()")) > 0 else None
            item["is_hide"] = tr.xpath("./td[position()=3]/text()")[0] if len(tr.xpath("./td[position()=3]/text()")) > 0 else None
            item["type"] = tr.xpath("./td[position()=4]/text()")[0] if len(tr.xpath("./td[position()=4]/text()")) > 0 else None
            item_list.append(item)

        return item_list

    # 检查代理的有效性
    def check_ip(self , item_list):
        # print(item_list)
        # 测试地址
        test_url = 'http://httpbin.org/ip'

        pool_list = []
        for item in item_list:
            # print("进入")
            # 代理地址
            proxys = {item["type"].lower(): "http://" + item["ip"] + ":" + item["socket"]}
            # print(proxys)
            # 随机选择一个代理地址
            user_agent = random.choice(self.user_agent_list)
            headers = {"User-Agent" : user_agent}

            try:
                response = requests.get(test_url , headers = headers , proxies = proxys , timeout = 5)
                if response.status_code == 200:
                    # 请求成功
                    html = response.content.decode("utf-8")
                    proxy_ip = json.loads(html)["origin"]
                    # print(proxy_ip)
                    if proxy_ip == item["ip"] :
                        print(item["ip"] + ":" + item["socket"] + "     可用")
                        # 放入列表中
                        pool_list.append(item)
                    else:
                        print('%s 携带代理失败,使用了本地IP' % (proxy_ip))
                else:
                    print(item["ip"] + ":" + item["socket"] + "     不可用")

            except Exception as e:
                print(item["ip"] + ":" + item["socket"] + "不可用")


        return pool_list

    # 保存item_list到文件中
    def save_pool(self , item_list , filename):
        with open(filename , "a" , encoding="utf-8") as f:
            for item in item_list:
                f.write(json.dumps(item , ensure_ascii=False))
                f.write("\n")

            print("保存成功")

    #读取硬盘上的item_list
    def get_item_list_from_file(self , filename):
        item_list = []
        content = ""
        with open(filename , "r" , encoding="utf-8") as f:
            for line in f.readlines():
                item = {}
                item = json.loads(line)
                item_list.append(item)

        return item_list


    def get_ip_info(self):
        url = "http://httpbin.org/ip"
        # url = "https://ip.cn/"
        # url = "https://www.baidu.com"
        proxies = {'http': 'http://27.208.91.189:8060'}

        # proxies = {'http': 'http://39.137.69.10:80'}


        response = requests.get(url , headers = self.headers , proxies = proxies)
        print(response.status_code)

        html = response.content.decode("utf-8")
        print(json.loads(html)["origin"])







    # 实现主要逻辑
    def run(self):

        # begin , 提取代理对象 , item , 开始***************************
        # 目标地址
        url = "http://www.ip3366.net/?stype=1&page=3"
        # 获取html页面源码
        html_str = self.get_html_source(url)
        # 提取数据为对象
        item_list = self.get_item_list(html_str)

        # item_list = [{'ip': '203.81.68.242', 'socket': '48388', 'location': '亚太地区', 'is_hide': '高匿代理IP', 'type': 'HTTPS'},
        #              {'ip': '117.131.235.198', 'socket': '8060', 'location': 'SSL高匿_亚太地区', 'is_hide': '高匿代理IP', 'type': 'HTTP'},
        #              {'ip': '39.137.69.10', 'socket': '80', 'location': 'SSL高匿_亚太地区', 'is_hide': '高匿代理IP', 'type': 'HTTP'}]
        # print(item_list)
        # end ********************************************************

        # 验证可用的ip
        pool_list = self.check_ip(item_list)

        # 对象持久化
        self.save_pool(pool_list , "proxy_pool.json")




if __name__ == '__main__':
    pool = ProxyIPPool()
    # pool.run()
    # pool.get_ip_info()


    item_list = pool.get_item_list_from_file("proxy_pool.json")
    # print(item_list)
    pool.check_ip(item_list)

