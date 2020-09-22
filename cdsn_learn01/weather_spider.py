#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/8 14:11
software: PyCharm
description: 
'''
import requests
from pymongo import MongoClient
from lxml import etree
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import win32api, win32gui

ct = win32api.GetConsoleTitle()

hd = win32gui.FindWindow(0,ct)

win32gui.ShowWindow(hd,0)

client = MongoClient()
db = client.learnTest
collection = db.city_code

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

def get_page(url):
    '''
    :param url: 爬取网址
    :return: text
    '''
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        if 200 == response.status_code:
            return response.text
    except:
        return None

def read_mongo(name):
    '''
    根据城市名称读取城市代码
    :param name:
    :return: 返回城市代码
    '''
    result = collection.find_one({'name': name})
    return result


def get_weather(url):
    text = get_page(url)

    html = etree.HTML(text)
    # result = html.xpath('//li[@class="sky skyid lv2 on"]')[0]
    try:
        result = html.xpath('//li[@class="sky skyid lv3 on"]')[0]
    except:
        result = html.xpath('//li[@class="sky skyid lv2 on"]')[0]

    wea = result.xpath('p[@class="wea"]/text()')[0].replace('\n', '').replace('\t', '')
    tem = result.xpath('p[@class="tem"]')[0].xpath('string(.)').replace('\n', '').replace('\t','')  # string()提取多个子节点中的文本
    win = result.xpath('p[@class="win"]')[0].xpath('string(.)').replace('\n', '').replace('\t', '')
    return (wea, tem, win)

def format_addr(s):
    name, addr = parseaddr(s)   #解析字符串中的email地址
    # email.utils.parseaddr('"Lao Wang" <tim_spac@126.com>')
    # ('Lao Wang', 'tim_spac@126.com')
    return formataddr((Header(name, 'utf-8').encode(), addr))#与parseaddr作用相反

def send_email(mess ,to_addr):
    # SMTP服务器以及相关配置信息
    smtp_server = 'smtp.163.com'    #163邮箱用到的SMTP服务器
    from_addr = 'hkyy521@163.com'
    password = '12345678'      #上面代码中发送方是163邮箱，所以密码不是邮箱的登录密码，而是手动开启SMTP协议后设置或分配的授权码！，但如果是Gmail则使用的密码是登录密码
    # to_addr = '1739468244@qq.com'

    msg = MIMEText(mess, 'plain', 'utf-8')
    # 如果没有加入如下代码，则会被识别为垃圾邮件
    # 1.创建邮件(写好邮件内容、发送人、收件人和标题等)
    msg['From'] = format_addr('天气卫士 <%s>' % from_addr)  # 发件人昵称和邮箱
    msg['To'] = format_addr('管理员 <%s>' % to_addr)  # 收件人昵称和邮箱
    msg['Subject'] = Header('来自acorn的问候……', 'utf-8').encode()  # 邮件标题

    # 2.登录账号
    server = smtplib.SMTP(smtp_server, 25)
    # server = smtplib.SMTP_SSL(smtp_server, 465)
    # server.set_debuglevel(1)#set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息
    server.login(from_addr, password)
    # 3.发送邮件
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == '__main__':
    name = "荆州"
    city = read_mongo(name)
    print(city)
    city_base_url = 'http://www.weather.com.cn/weather/{}.shtml'
    curl = city_base_url.format(city['id'])
    wea, tem, win = get_weather(curl)
    mess = "{0}——天气：{1}，气温：{2}，风级：{3}".format(name, wea, tem, win)
    to_addr = '1739468244@qq.com'
    send_email(mess,to_addr)
