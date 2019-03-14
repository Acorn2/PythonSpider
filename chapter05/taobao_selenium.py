#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 14:27
software: PyCharm
description: 
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import json

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KeyWord = 'iPad'

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
        # browser.get(url)
        # add_cookies()
        if page > 1:
            input = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span',str(page))))
        wait.until(EC.presence_of_element_located(By.CSS_SELECTOR,'.m-itemlist .items .item'))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    #提取商品数
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic.img').attr('data-src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)

if __name__ == '__main__':
    browser.get('https://www.taobao.com')
    add_cookies()
    input = browser.find_element_by_id('q')
    input.send_keys(KeyWord)
    button = browser.find_element_by_class_name('btn-search')
    button.click()
    index_page(1)
    # url = 'https://www.taobao.com/search?q=' + quote(KeyWord)
    # browser.get(url)