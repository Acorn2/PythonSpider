#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/8 15:56
software: PyCharm
description: 
'''
import requests
from pyquery import PyQuery as pq
import re
from pymongo import MongoClient
import time
from lxml import etree
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

client = MongoClient()
db = client.learnTest
collection = db.city_code

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

places = ['hb', 'db', 'hd', 'hz', 'hn', 'xb', 'xn', 'gat']  # 全国按照8大地区进行划分


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


def parse_url(url):
    '''
    查询每个地区的省会url，下一步进行跳转
    :param url:
    :return: 省会urls
    '''
    provinces = []
    text = get_page(url)
    doc = pq(text)

    # body > div.lqcontentBoxH > div.contentboxTab > div > div > div.hanml > div:nth-child(1) > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.rowsPan > a
    items = doc('.conMidtab2 > table > tr:nth-child(3) > td.rowsPan').items()
    # items = doc('.conMidtab2 > table').items()

    name_set = set()
    for item in items:  # 天气页面显示未来7天的天气，我们需要的数据只需要取其一
        province_url = 'http://www.weather.com.cn' + item.find('a').attr('href')
        province_name = item.find('a').text()
        province = {
            'province_url': province_url,
            'province_name': province_name
        }
        if province_name not in name_set:
            name_set.add(province_name)
            provinces.append(province)
        else:
            break
    return provinces


def get_city_id(curl):
    '''
    读取每个省下的城市信息
    :param curl:
    :return: 城市代码和名称
    '''
    cities = []
    text = get_page(curl)

    # content = re.search(r'<div.*?class="conMidtab3".*?>(.*?)</div>',text,re.S)#由于当前页面可以显示未来7天的天气情况，所以我们在此仅选取第一天的内容
    # print(type(content))
    # print(len(content.groups()))
    # new_text = ''.join(content.groups())
    pattern = re.compile('<td width="83" height="23".*?<a.*?href=".*?weather/(.*?).shtml".*?>(.*?)</a></td>', re.S)
    results = re.findall(pattern, text)

    n = 0
    name_set = set()
    for item in results:
        id = item[0]
        name = item[1]
        city = {
            'id': id,
            'name': name
        }
        if name not in name_set:
            name_set.add(name)
            cities.append(city)
        else:
            continue

    return cities


def save_to_mongo(cities):
    '''
    将城市代码以及城市名称存储在mongodb中
    :param cities:
    :return:
    '''
    for city in cities:
        try:
            collection.insert_one(city)
        except Exception as e:
            print(e)


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
    result = html.xpath('//li[@class="sky skyid lv3 on"]')[0]

    wea = result.xpath('p[@class="wea"]/text()')[0].replace('\n', '').replace('\t', '')
    tem = result.xpath('p[@class="tem"]')[0].xpath('string(.)').replace('\n', '').replace('\t','')  # string()提取多个子节点中的文本
    win = result.xpath('p[@class="win"]')[0].xpath('string(.)').replace('\n', '').replace('\t', '')
    return (wea, tem, win)

def format_addr(s):
    name, addr = parseaddr(s)   #解析字符串中的email地址
    # email.utils.parseaddr('"Lao Wang" <tim_spac@126.com>')
    # ('Lao Wang', 'tim_spac@126.com')
    return formataddr((Header(name, 'utf-8').encode(), addr))#与parseaddr作用相反

def send_email(mess):
    # SMTP服务器以及相关配置信息
    smtp_server = 'smtp.163.com'    #163邮箱用到的SMTP服务器
    from_addr = 'hkyy521@163.com'
    password = 'gzy521695'      #上面代码中发送方是163邮箱，所以密码不是邮箱的登录密码，而是手动开启SMTP协议后设置或分配的授权码！，但如果是Gmail则使用的密码是登录密码
    to_addr = '1739468244@qq.com'

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
    base_url = 'http://www.weather.com.cn/textFC/{}.shtml'

    # cities = []
    # print("城市信息爬取开始....")
    # for it in places:
    #     url = base_url.format(it)#每个大地区的网页
    #     print(url)
    #     provinces = parse_url(url)
    #     for i in range(len(provinces)):#每个省份的页面
    #         purl = provinces[i]['province_url']#省url
    #         pname = provinces[i]['province_name']#省名称
    #         each_provice = get_city_id(purl)
    #         print("{0}共有{1}个市级/县级行政区".format(pname,len(each_provice)))
    #         cities.extend(each_provice)
    #     time.sleep(2)
    #
    # print("城市信息爬取完毕，开始存储到mongo中......")
    # save_to_mongo(cities)
    # print("信息存储完毕！")

    # name = input("请输入需要查询天气的城市名称：\n")
    name = "枣阳"
    city = read_mongo(name)
    city_base_url = 'http://www.weather.com.cn/weather/{}.shtml'
    curl = city_base_url.format(city['id'])
    wea, tem, win = get_weather(curl)
    mess = "{0}——天气：{1}，气温：{2}，风级：{3}".format(name,wea, tem, win)
    send_email(mess)
