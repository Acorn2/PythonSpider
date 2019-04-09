#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/14 20:34
software: PyCharm
description:利用Selenium模拟登录淘宝并获取所有订单,目前cookie使用有时效性，过会就不能使用了
关于webdriver.Chrome()方法使用
参考网址：https://blog.csdn.net/u012995964/article/details/84973774
'''

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import \
    expected_conditions as EC  # 具体介绍参考：https://blog.csdn.net/kelanmomo/article/details/82886718
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import json
from pymongo import MongoClient
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KeyWord = 'iPad'

client = MongoClient()
db = client.learnTest
collection = db.taobao_product


# 这是个人登录淘宝网址时，保留的cookie文件，这里我使用的是谷歌浏览器，安装EditThisCookie插件，把登录时的cookie保存下来
def add_cookies():
    with open('taobao.json', 'rb') as f:
        cookies = json.load(f)
        for item in cookies:
            browser.add_cookie(item)


# 进入淘宝首页后，需要再进入我的订单
def get_orderPage():
    myTaobao = browser.find_element_by_partial_link_text('我的淘宝')  # 查找含有超链接文本的元素;仅限当前页面上显示的，鼠标箭头滑动展示的新内容，无法使用
    myTaobao.click()

    time.sleep(3)
    button = browser.find_element_by_partial_link_text('已买到的宝贝')
    button.click()


def index_page(page):
    print('正在爬取第', page, '页')
    try:
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))  # 找到页面底部页数跳转输入框
            submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))  # 输入页数后，点击确定进行跳转
            input.clear()
            input.send_keys(page)
            submit.click()
        # 判断当前高亮的页码数是当前的页码数即可，所以这里使用了另一个等待条件text_to_be_present_in_element，它会等待指定的文本出现在某一个节点里面时即返回成功。
        # 这里我们将高亮的页码节点对应的CSS选择器和当前要跳转的页码通过参数传递给这个等待条件，这样它就会检测当前高亮的页码节点是不是我们传过来的页码数，
        # 如果是，就证明页面成功跳转到了这一页，页面跳转成功。
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.row-mod .pagination-item-active > a'), str(page)))
        # tp-bought-root > div.row-mod__row___30Zj1.js-actions-row-bottom > div:nth-child(2) > ul > li.pagination-item.pagination-item-1.pagination-item-active > a
        # 我们最终要等待商品信息加载出来，就指定了presence_of_element_located这个条件，然后传入了.m-itemlist .items .item这个选择器，而这个选择器对应的页面内容就是每个商品的信息块，
        # 可以到网页里面查看一下。如果加载成功，就会执行后续的get_products()方法，提取商品信息。
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tp-bought-root .index-mod__orde')))
        # tp-bought-root > div:nth-child(7)
        get_orders()
    except TimeoutException:
        index_page(page)


# 提取订单信息
def get_orders():
    html = browser.page_source
    doc = pq(html)
    # 提取了商品列表，此时使用的CSS选择器是#mainsrp-itemlist .items .item，它会匹配整个页面的每个商品。它的匹配结果是多个
    items = doc('#tp-bought-root .index-mod__orde').items()  # 关于css选择器，可以模糊匹配

    # for item in items:
    #     order = {
    #         'create_time':item.find('.bought-wrapper-mod .create-time').text(),#订单日期
    #         # tp-bought-root > div:nth-child(7) > div > table > tbody.bought-wrapper-mod__head___2vnqo > tr > td.bought-wrapper-mod__head-info-cell___29cDO > span > span:nth-child(3)
    #         'order_num':item.find('.bought-wrapper-mod ').text().strip().replace('\n',''),#订单编号
    #         'shop':item.find('.bought-wrapper-mod .seller-mod__name').text(),#卖家店铺
    #         # tp-bought-root > div:nth-child(7) > div > table > tbody:nth-child(3) > tr > td:nth-child(1) > div > div:nth-child(2) > p:nth-child(1) > a > span:nth-child(2)
    #         # tp-bought-root > div:nth-child(8) > div > table > tbody:nth-child(3) > tr > td:nth-child(1) > div > div:nth-child(2) > p:nth-child(1) > a > span:nth-child(2)
    #         'title':item.find('.ml-mod_container > div:nth-child(2) > p:nth-child(1) > a ').text().strip().replace('\n',','),#宝贝名称
    #         'unit-price':item.find('.sol-mod .price > p').text(),#单价
    #         # tp-bought-root > div:nth-child(8) > div > table > tbody:nth-child(3) > tr > td:nth-child(3) > div > p
    #         'number':item.find('.bought-table > tbody:nth-child(3) > tr > td:nth-child(3) > div > p').text(),#购买数量
    #         # tp-bought-root > div:nth-child(7) > div > table > tbody:nth-child(3) > tr > td:nth-child(5) > div > div.price-mod__price___157jz > p > strong > span:nth-child(2)
    #         'pay':item.find('.bought-table > tbody:nth-child(3) > tr > td:nth-child(5) .price > p > strong').text()#实际付款
    #     }


# 将爬取的结果存入mongodb中
def save_to_mongo(product):
    try:
        collection.insert_one(product)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("淘宝模拟登录，搜索ipad物品，爬取一定页数的产品简介....")
    browser.get('https://www.taobao.com')
    add_cookies()
    # J_SiteNavMytaobao > div.site-nav-menu-bd.site-nav-menu-list > div > a:nth-child(1)
    # button = browser.find_element_by_css_selector ('.site-nav-menu-bd .site-nav-menu-list > div > a:nth-child(1)')
    # J_SiteNavMytaobao > div.site-nav-menu-hd > a
    # J_SiteNavMytaobaom
    button = browser.find_element_by_css_selector('.site-nav-bd-r #J_SiteNavMytaobao .site-nav-menu-hd > a')
    button.click()
    # get_orderPage()
    # index_page(1)
    # button = browser.find_element_by_class_name('btn-search')

    browser.close()

    # print("内容爬取完毕，已经存入数据库中！")
