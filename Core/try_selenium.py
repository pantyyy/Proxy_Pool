# coding=utf-8
from selenium import webdriver
import time


#实例化一个浏览器
driver = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')


#发送请求
driver.get("http://www.baidu.com")

#元素定位的方法
driver.find_element_by_id("kw").send_keys("python")
# driver.find_element_by_id("su").click()

#退出浏览器
time.sleep(3)
driver.quit()