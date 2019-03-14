#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 16:39
software: PyCharm
description: 百度贴吧内容爬取（主要包含发帖人名称，发帖人等级，发帖内容）
'''

import requests,re
import json

# ----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")

    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("<", "<"), (">", ">"), ("&", "&"), ("&", "\""), (" ", " ")]

    def Replace_Char(self, x):
        x = self.BgnCharToNoneRex.sub("", x)
        x = self.BgnPartRex.sub("\n    ", x)
        x = self.CharToNewLineRex.sub("\n", x)
        x = self.CharToNextTabRex.sub("\t", x)
        x = self.EndCharToNoneRex.sub("", x)

        for t in self.replaceTab:
            x = x.replace(t[0], t[1])
        return x

class Baidu_Spider():
    #申明类的属性
    def __init__(self,url):
        # self.myUrl = url +"?see_lz=1"
        self.myUrl = url
        self.datas = []
        self.myTool = HTML_Tool()
        print("已启动百度贴吧爬虫，卡擦卡擦")

    #初始化加载页面并将其转码存储
    def baidu_tieba(self):
        try:
            myPage = requests.get(self.myUrl)
            if myPage.status_code == 200:
                html = myPage.text
        except requests.ConnectionError:
            html = ""
        # 计算楼主发布内容一共有多少页
        endPage = self.page_counter(html)
        # 获取该帖的标题
        title = self.find_title(html)
        print("文章名称：" + title)
        # 获取最终的数据
        self.save_data(self.myUrl, title, endPage)


    def page_counter(self,myPage):
        myMatch = re.search(r'<span class="red">(\d+?)</span>',myPage,re.S)
        if myMatch:
            endPage = int(myMatch.group(1))
            print("爬虫报告：发现楼主共有%d页的原创内容" %endPage)
        else:
            endPage = 0
            print("爬虫报告：无法计算楼主发布内容有多少页！")

        return endPage

    def find_title(self,myPage):
        myMatch = re.search(r'<h3.*?>(.*?)</h3>',myPage,re.S)
        title = '暂无标题'
        if myMatch:
            title = myMatch.group(1)
        else:
            print("爬虫报告：无法加载文章标题！")

        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace(
                '"', '').replace('>', '').replace('<', '').replace('|', '')
        return title

    def get_data(self,url,endPage):
        # url = url + "&pn="
        url = url + "?pn="
        for i in range(1,endPage):
            print("爬虫报告：爬虫%d号正在加载中..." %i)
            try:
                myPage = requests.get(url + str(i))
                if myPage.status_code == 200:
                    html = myPage.text
                    # print(myPage)
            except requests.ConnectionError:
                html = ""
            # 将myPage中的html代码处理并存储到datas里面
            # print(html)
            self.deal_data(html)

    def deal_data(self,myPage):
        pattern = re.compile('<li class="d_name".*?<a.*?>(.*?)</a>.*?class="d_badge_lv">(.*?)</div>.*?<div id="post_content.*?>(.*?)</div>',re.S)
        # pattern = re.compile('<div id="post_content.*?>(.*?)</div>',re.S)
        # pattern = re.compile('<li class="d_name".*?<a.*?>(.*?)</a>.*?class="d_badge_lv">(.*?)</div>',re.S)
        results = re.findall(pattern,myPage)
        for item in results:
            # print(item)
            each_data = {
                'author':self.myTool.Replace_Char(item[0].strip()),#发帖人名称
                'grade':item[1].strip(),#发帖人等级
                'content':self.myTool.Replace_Char(item[2].replace('\n',''))#发帖内容
            }
            # print(each_data)
            self.datas.append(each_data)

    def save_data(self,url,title,endPage):
        self.get_data(url, endPage)
        with open('baidu_tieba.txt', 'w', encoding='utf-8') as f:
            for item in self.datas:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print("贴吧内容爬取完毕！")


if __name__ == '__main__':
    # -------- 程序入口处 ------------------
    print
    u"""#---------------------------------------
    #   程序：百度贴吧爬虫
    #   版本：0.5
    #   作者：acorn
    #   日期：2013-05-16
    #   语言：Python 3.7
    #   操作：输入网址后自动只看楼主并保存到本地文件,也可爬取所有
    #   功能：将楼主发布的内容打包txt存储到本地。
    #---------------------------------------
    """
    # see_lz=1是只看楼主，pn=1是对应的页码
    print('请输入贴吧的地址最后的数字串：')
    # bdurl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
    # bdurl = 'https://tieba.baidu.com/p/4305104425?see_lz=1&pn=1'
    bdurl = 'https://tieba.baidu.com/p/4305104425'

    # 调用
    mySpider = Baidu_Spider(bdurl)
    mySpider.baidu_tieba()