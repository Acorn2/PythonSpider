#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/15 16:17
software: PyCharm
description: 虾米音乐歌单爬取，暂时还无法实现下载功能，url地址无法提取
'''

import requests,re
from pyquery import PyQuery as pq
import sys
import jieba


def get_page(url):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control' : 'max-age=0',
        'cookie' : 'gid=155045794549798; _unsign_token=b8535ae630f96bfb467d45def43f3d0c; xmgid=c25ef830-239f-43b3-ba82-020f6ba9acea; cna=X+/vE/XpfxICAXWQe23tejwg; PHPSESSID=bdf27756d33738daebbf5d645a17861d; _xiamitoken=6dd994147dade882109ffd638fb68e25; UM_distinctid=16980614eb47c6-064321ba7b2dab-9333061-1fa400-16980614eb5a74; _xm_umtoken=T5F4188A4CAB630D35FEC4FE30FF337837C8E51C8D7D6A9189C82C50D6A; l=bBxiCnX4vmdsVnrxBOCwiuIRXQQT7IRAguPRwk_Ji_5CA6T1W8XOl1xLCF96Vj5R_tLB4-L8Y1y9-etkw; xm_sg_tk=d81fe0c1f3e4fc8abad7c0d64491c708_1552649892427; xm_sg_tk.sig=SlPkHzaVqAr_gAoTymsjcJWXavUQPIkYITNP2YLVK-Q; isg=BCIijDWGivaYapbLgHCUulAgc6hE2w099dNX2Gy8CRXnP8i5VgIInKn2bjtmBJ4l',
        'referer': 'https://www.xiami.com/list/artist',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        response = requests.get(url,headers=headers)
        if 200 == response.status_code:
            return response.text
    except requests.ConnectionError as e:
        return None

#获取排行榜上的一些信息
def get_content(text):
    doc = pq(text)
    #标签不完全一致
    items = doc('.billboard-songs .table-container .odd').items()
    odd_data = []
    for item in items:
        song = {
            'index': item.find('.em.index').text(),
            'name': item.find('.song-name').text(),
            'url' : 'https://www.xiami.com'+item.find('.song-name > a ').attr('href'),
            'singer': item.find('.singers').text(),
            'time': item.find('.duration-container .duration ').text()
        }
        print(song)
        odd_data.append(song)

    even_data = []
    items = doc('.billboard-songs .table-container .even').items()
    for item in items:
        song = {
            'index': item.find('.em.index').text(),
            'name': item.find('.song-name').text(),
            'url': 'https://www.xiami.com' + item.find('.song-name > a ').attr('href'),
            'singer': item.find('.singers').text(),
            'time': item.find('.duration-container .duration ').text()
        }
        print(song)
        even_data.append(song)

    all_datas = []
    for i in range(len(odd_data)):
        if odd_data[i]:
            all_datas.append(odd_data[i])
        if even_data[i]:
            all_datas.append(even_data[i])

    return all_datas

def get_song(url):
    html = get_page(url)
    doc = pq(html)

    name = doc('#title > h1').text()
    result = doc('.lrc_main').text()
    print(name.replace('MV',''))
    return result.split('\n')

def jieba_deal(content):
    all_words = []
    num = 0
    for line in content:
        if line.strip():
            num += 1
            # print("*********正在处理第{}行数据*********".format(str(num)))
            line_data = ''
            line_jiebas = jieba.cut(line)
            for i in line_jiebas:
                if i >= u'\u4e00' and i <= u'\u9fa5':
                    line_data += i + ' '
                    all_words.append(i)
    return all_words

def get_TF(words):
    dict_num = {}
    for word in words:
        if word not in dict_num:
            dict_num[word] = 1
        else:
            dict_num[word] += 1

    dict_num = sorted(dict_num.items(),key=lambda d:d[1],reverse=True)
    for key in dict_num:
        print("{0}:{1}".format(key[0],str(key[1])))

if __name__ == '__main__':
    # url = 'https://www.xiami.com/list/artist'
    # url = 'https://www.xiami.com'
    page = 1
    # url = 'https://www.xiami.com/billboard/102'
    # url = 'https://www.xiami.com/billboard/103'
    print(u''
          '************虾米音乐爬取************\n'
          '1.新歌榜\n'
          '2.热歌榜\n'
          '3.电音榜\n'
          '4.歌单收录榜\n'
          '5.抖音热歌榜\n'
          '6.影视原声榜\n'
          '7.虾米分享榜')
    # music_url  = int(input('请输入数字：\n'))
    #
    # if music_url == 0:
    #     # 新歌榜
    #     url = "https://www.xiami.com/billboard/102"
    # elif music_url == 1:
    #     # 热歌榜
    #     url = "https://www.xiami.com/billboard/103"
    # elif music_url == 2:
    #     # 电音榜
    #     url = "https://www.xiami.com/billboard/325"
    # elif music_url == 3:
    #     # 歌单收录榜
    #     url = "https://www.xiami.com/billboard/306"
    # elif music_url == 4:
    #     # 抖音热歌榜
    #     url = "https://www.xiami.com/billboard/332"
    # elif music_url == 5:
    #     # 影视原声榜
    #     url = "https://www.xiami.com/billboard/324"
    # elif music_url == 6:
    #     # 虾米分享榜
    #     url = "https://www.xiami.com/billboard/307"
    #
    # text = get_page(url)
    # get_content(text)

    # get_song('https://www.xiami.com/song/mSzHs4ed511')
    url = 'https://www.xiami.com/song/mSzHs4ed511'
    url = url.replace('www','emumo')
    content = get_song(url)
    words = jieba_deal(content)
    get_TF(words)