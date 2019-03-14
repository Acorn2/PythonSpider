#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/11 8:50
software: PyCharm
description: 糗事百科24小时段子爬取
'''

import requests,re,time
import threading
import _thread
import json


class Choushi_Spider:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

    def getPage(self,page):
        myurl = "http://m.qiushibaike.com/hot/page/"+page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        try:
            res = requests.get(myurl,headers=headers)
            if res.status_code == 200:
                return res.text
            else:
                return None
        except requests.ConnectionError:
            return None

    #处理当前爬取的页面信息
    def dealPage(self,content):
        pattern = re.compile('<div.*?class="author.*?<h2>(.*?)</h2>.*?<div.*?class="articleGender.*?>(.*?)</div>.*?<div.*?class="content">\n+<span>(.*?)</span>\n+</div>'
                             '.*?<span.*?class="stats-vote">.*?<i.*?>(.*?)</i>.*?<span.*?class="stats-comments">.*?<i.*?>(.*?)</i>',re.S)
        results = re.findall(pattern,content)
        each_page = []
        for item in results:
            each_data = {
                'author':item[0].strip(),
                'grade':item[1].strip(),
                'content':item[2].strip(),
                'vote':item[3].strip(),
                'comments':item[4].strip()
            }
            each_page.append(each_data)
        return each_page

    #加载新的段子
    def loadPage(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.getPage(str(self.page))
                    results = self.dealPage(myPage)
                    self.page += 1
                    self.pages.append(results)
                except:
                    print("无法链接糗事百科！")
            else:
                time.sleep(30)

    #段子信息展示
    def showPage(self,nowPage,page):
        for i in range(0,len(nowPage)):
            item = "\n"+nowPage[i]["content"].replace("\n","").replace("<br/>","\n")+"\n\n"
            print("第%d页，第%d个故事" %(page,(i+1)))
            print(item)

        myInput = str(input("回车键看下一页，按esc退出："))
        if myInput == 'quit':
            self.enable = False

    #不限次的爬取笑话
    def start(self):
        self.enable = True
        page = self.page

        print("正在加载中请稍后........")

        # threading.Thread(target=self.loadPage)
        _thread.start_new_thread(self.loadPage,())
        while self.enable:
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.showPage(nowPage,page)
                page += 1

    def savePage(self):
        with open('choushi.json','w',encoding='utf-8') as fw:
            for each_page in self.pages:
                for item in each_page:
                    fw.write(json.dumps(item,ensure_ascii=False))

if __name__ == '__main__':
    print
    """ 
        --------------------------------------- 
               程序：糗百爬虫 
               版本：0.4 
               作者：acorn
               日期：2019-03-11 
               语言：Python 3.7 
               操作：输入quit退出阅读糗事百科 
               功能：按下回车依次浏览今日的糗百热点 
        --------------------------------------- 
    """
    print("请按下回车浏览今日的糗百内容：")
    input("")
    model = Choushi_Spider()
    # page = model.getPage(str(1))
    # each_page = model.dealPage(page)
    # for item in each_page:
    #     print(item)
    model.start()
