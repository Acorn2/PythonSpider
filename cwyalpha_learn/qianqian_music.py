#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/18 9:22
software: PyCharm
description: 爬取千千音乐分类中心情分类的歌单，对各个歌单下的歌曲进行歌词爬取，利用jieba分词对歌词进行分词处理，根据TF值汇总出每个心情分类下的关键词
'''

import requests
from pyquery import PyQuery as pq
import jieba
from urllib.parse import quote
from urllib.parse import urlencode
import time,os
from hashlib import md5
from urllib.request import urlretrieve

class Qianqian:
    def __init__(self):
        self.baseUrl = 'http://music.taihe.com/tag/'
        self.titles = ['伤感','激情','安静','舒服','甜蜜','励志','寂寞','想念','浪漫','怀念','喜悦','深情','美好','怀旧','轻松']
        self.flag = True

    #获取各个心情分类下的歌单
    def get_text(self,start,url):
        params = {
            'start': start,
            'size': '20',
            'third_type': '0'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        if self.flag:
            url = self.baseUrl + quote(self.titles[0]) +'?' + urlencode(params)

        try:
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            if 200 == response.status_code:
                return response.text
        except requests.ConnectionError as e:
            time.sleep(1)
            return None

    #处理歌单，提取有用信息，包括歌名，详细url，歌手
    def get_songList(self):
        songList = []
        self.flag = True
        for page in range(0,10):
            print("**********正在爬取第{0}页的歌单信息**********".format(str(page+1)))
            start = page * 20
            html = self.get_text(start,None)
            doc = pq(html)

            items = doc('.song-list .song-item-hook').items()

            for item in items:
                # first_song_li > div > span.song-title > a:nth-child(1)
                song = {
                    'name' : item.find('.song-item  .song-title > a:nth-child(1)').text(),
                    'url' : 'http://music.taihe.com' + item.find('.song-item  .song-title > a:nth-child(1)').attr('href'),
                    'singer' : item.find('.author_list').text()
                }
                print(song)
                songList.append(song)
        return songList

    #获取每首歌的歌词链接
    def get_lyric(self):
        songList = self.get_songList()
        print("爬取{0}主题下的歌单结束，一共爬取了{1}首歌曲".format(self.titles[0],len(songList)))

        print("开始爬取每首歌的歌词信息......")
        lyric_url_list = []
        self.flag = False
        for song in songList:
            url = song['url']
            html = self.get_text(None,url)

            doc = pq(html)
            lyric_url = doc('#lyricCont').attr('data-lrclink')
            lyric_url_list.append(lyric_url)

        # html = self.get_text(None, 'http://music.taihe.com/song/121353608')
        # html = self.get_text(None, 'http://music.taihe.com/song/121001284')
        #
        # doc = pq(html)
        # lyric_url = doc('#lyricCont').attr('data-lrclink')
        return songList,lyric_url_list

    #下载歌词
    def download_lyric(self,title):
        catalog = "qianqian_music/" + title
        if not os.path.exists(catalog):
            os.mkdir(catalog)

        songList,lyric_url_list = self.get_lyric()
        print("歌词url信息爬取结束，开始下载歌词到本地！")

        if len(songList) == len(lyric_url_list):
            for i in range(len(lyric_url_list)):
                lyric_url = lyric_url_list[i]
                song_name = songList[i]['name']
                if lyric_url == None:
                    print("该歌曲暂时没有歌词，跳过....")
                else:
                    # song_name = '半壶纱'
                    # song_name = '愿做菩萨那朵莲'
                    html = self.get_text(None,lyric_url)

                    file = catalog + '/' + song_name

                    # file_path = '{0}.{1}'.format(file, 'text')
                    # urlretrieve(lyric_url,file_path)#函数参数可以传入一个回调函数，用于显示下载进度。但是不确定文件下载时会不会自动关闭工作流之类的
                    #存在问题：下载文件不完全且避免下载时长过长陷入死循环
                    try:
                        response = requests.get(lyric_url)
                        if 200 == response.status_code:
                            file_path = '{0}.{1}'.format(file, 'txt')
                            if not os.path.exists(file_path):
                                with open(file_path, 'wb') as fw:
                                    fw.write(response.content)
                                    print("《{0}》歌曲的歌词下载完毕！".format(song_name))
                            else:
                                print('Already Download', file_path)
                    except requests.ConnectionError:
                        print('Failed to Save Text')

    #读取每个心情分类下的歌词文件，将歌词信息按行存入到List中
    def read_lyric(self,title):
        catalog = "\qianqian_music\\" + title
        filepath = os.path.abspath('.') +catalog #获取当前文件工作目录路径+歌词文件夹路径
        lists = os.listdir(filepath)

        all_messages = []
        for i in range(0,len(lists)):
            print("正在读取第{0}个文件.....".format(str(i+1)))
            path = os.path.join(filepath,lists[i])
            if os.path.isfile(path):
                with open(path,encoding='utf-8') as fr:
                    data = fr.readlines()
                    for line in data:
                        line = line.strip()
                        if "[00:" in line:
                            if "唱：" in line or "词:" in line or "曲:" in line or "行：" in line or "词：" in line or"曲：" in line :
                                pass
                            else:
                                all_messages.append(line)
        return all_messages

    def get_jieba(self,content):
        print("歌词信息读取完毕，接下来使用jieba分词进行处理......")
        all_words = []

        stopw_file = 'E:\PycharmWspace\PythonSpider\cwyalpha_learn\stopwords.txt'
        stopwords_file = open(stopw_file,encoding='utf-8')
        stopwords = stopwords_file.read().split('\n')

        for line in content:
            if line.strip():
                line_data = ''
                line_jiebas = jieba.cut(line)
                for i in line_jiebas:
                    if i >= u'\u4e00' and i <= u'\u9fa5':
                        if i not in stopwords:
                            line_data += i + ' '
                            all_words.append(i)
                if line_data.strip():
                    pass
                    # print(line_data)
        stopwords_file.close()
        return all_words

    def get_TF(self,datas):
        dict_num = {}
        for word in datas:
            if word not in dict_num:
                dict_num[word] = 1
            else:
                dict_num[word] += 1

        dict_num = sorted(dict_num.items(), key=lambda d: d[1], reverse=True)
        n = 0
        for key in dict_num:
            if n < 200:
                # print(key[0])
                print("{0}:{1}".format(key[0], str(key[1])))
            n += 1

    def start(self):
        for title in self.titles:
            pass

        #目前只爬取title[0]里的数据进行尝试分析，等学习爬虫框架后再来大批量爬取
        if not os.path.exists("qianqian_music"):
            os.mkdir('qianqian_music')
        print("开始爬取{0}主题下的歌单......".format(self.titles[0]))
        # self.download_lyric(self.titles[0])
        self.get_songList()
        print("歌词下载结束！")

        # print("开始爬取{0}目录下的歌词文件......".format(self.titles[0]))
        # content = self.read_lyric(self.titles[0])
        # datas = self.get_jieba(content)
        # print("对于分词后的歌词信息进行词频计算，提取词频前二十的词汇")
        # self.get_TF(datas)

if __name__ == '__main__':
    stime = time.time()
    qq = Qianqian()
    # qq.get_songList()
    # qq.get_lyric()
    # qq.download_lyric()
    # qq.read_lyric()
    # qq.get_jieba()
    qq.start()

    etime = time.time()
    print("总共耗时{}s".format(str(etime-stime)))
