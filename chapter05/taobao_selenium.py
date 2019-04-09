#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 14:27
software: PyCharm
description: 利用Selenium抓取淘宝商品并用pyquery解析得到商品的图片、名称、价格、购买人数、店铺名称和店铺所在地信息，并将其保存到MongoDB。
学习网址：https://blog.csdn.net/qq_29027865/article/details/83377660
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC#具体介绍参考：https://blog.csdn.net/kelanmomo/article/details/82886718
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import json
from pymongo import MongoClient
from urllib.parse import quote

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KeyWord = 'iPad'

client = MongoClient()
db = client.learnTest
collection = db.taobao_product

#这是个人登录淘宝网址时，保留的cookie文件，这里我使用的是谷歌浏览器，安装EditThisCookie插件，把登录时的cookie保存下来
def add_cookies():
    with open('taobao.json','rb') as f:
        cookies = json.load(f)
        for item in cookies:
            browser.add_cookie(item)

def index_page(page):
    """
       抓取索引页
       :param page: 页码
    """
    print('正在爬取第',page,'页')
    try:
        # url = 'https://s.taobao.com/search?q=' + quote(KeyWord)
        # print(url)
        # browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))#找到页面底部页数跳转输入框
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))#输入页数后，点击确定进行跳转
            input.clear()
            input.send_keys(page)
            submit.click()
        #判断当前高亮的页码数是当前的页码数即可，所以这里使用了另一个等待条件text_to_be_present_in_element，它会等待指定的文本出现在某一个节点里面时即返回成功。
        # 这里我们将高亮的页码节点对应的CSS选择器和当前要跳转的页码通过参数传递给这个等待条件，这样它就会检测当前高亮的页码节点是不是我们传过来的页码数，
        # 如果是，就证明页面成功跳转到了这一页，页面跳转成功。
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager .items .item.active .num'), str(page)))
        #我们最终要等待商品信息加载出来，就指定了presence_of_element_located这个条件，然后传入了.m-itemlist .items .item这个选择器，而这个选择器对应的页面内容就是每个商品的信息块，
        # 可以到网页里面查看一下。如果加载成功，就会执行后续的get_products()方法，提取商品信息。
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    html = browser.page_source
    doc = pq(html)
    #提取了商品列表，此时使用的CSS选择器是#mainsrp-itemlist .items .item，它会匹配整个页面的每个商品。它的匹配结果是多个
    items = doc('#mainsrp-itemlist .items .item').items()#关于css选择器，可以模糊匹配

    for item in items:
        product = {
            'image':item.find('.pic-link .img').attr('data-src'),#商品缩略图
            'price':item.find('.price').text().strip().replace('\n',''),#价格
            'deal':item.find('.deal-cnt').text(),#销售量
            'title':item.find('.title').text().strip().replace('\n',','),#简介
            'shop':item.find('.shop').text(),#商家
            'location':item.find('.location').text()#商家地址
        }
        print(product)
        # save_to_mongo(product)

#将爬取的结果存入mongodb中
def save_to_mongo(product):
    try:
        collection.insert_one(product)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print("淘宝模拟登录，搜索ipad物品，爬取一定页数的产品简介....")
    browser.get('https://www.taobao.com')
    add_cookies()
    input = browser.find_element_by_id('q')
    input.send_keys(KeyWord)
    button = browser.find_element_by_class_name('btn-search')
    button.click()
    print("淘宝模拟登录成功，查询完毕，现在开始爬取内容")
    for i in range(1,3):
        index_page(i)
    browser.close()

    print("内容爬取完毕，已经存入数据库中！")

