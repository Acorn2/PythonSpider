#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/11 17:23
software: PyCharm
description: 在百度学术网站下载论文参考文献
'''

import requests,os,re
from collections import namedtuple
from urllib.parse import urlencode
from urllib import parse
from bs4 import BeautifulSoup
import json

def get_page(keywords,offset):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    params = {
        'wd': keywords,
        'pn':offset,
        'tn':'SE_baiduxueshu_c1gjeupa',
        'ie':'utf-8',
        'sc_hit':'1'
    }
    url = "http://xueshu.baidu.com/s?"+urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None

#经尝试，本程序适合使用BeautifulSoup来爬取相应的内容
def get_images(text):
    # pattern = re.compile('<div.*?class="sc_content".*?<h3.*?><a.*?href="(.*?)".*?>(.*?)</a></h3>.*?</div>',re.S)
    pattern = re.compile('<div.*?class="sc_content">.*?<h3.*?><a.*?href="(.+?)".*?>.*?</h3>.*?</div>',re.S)
    results = re.findall(pattern,text.replace('\n','').strip())
    for item in results:
        print(item.encode('utf-8'))

#对于每页的文献信息（每页基本包含10篇文献），提取所有的文献主题、作者、摘要、文献详细地址
def get_urls(text):
    all_titles = []#主题
    all_abstracts = []#作者
    all_authors = []#摘要
    all_paper_urls = []#论文初步网址

    soup = BeautifulSoup(text,'lxml')

    title_datas = soup.select('div.sc_content > h3 > a')#select返回值类型为<class 'list'>

    author_datas = soup.find_all('div','sc_info')#find_all返回值类型为<class 'bs4.element.ResultSet'>

    abstract_datas = soup.find_all('div','c_abstract')
    for item in title_datas:
        result = {
            'title':item.get_text(),
            'href':item.get('href')#关于论文的详细网址，经过观察发现需要提取部分内容
            #http://xueshu.baidu.com/usercenter/paper/show?paperid=389ef371e5dae36e3a05b187f7eb2a95&site=xueshu_se
            #/s?wd=paperuri%3A%28389ef371e5dae36e3a05b187f7eb2a95%29&filter=sc_long_sign&sc_ks_para=q%3D%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E7%A0%94%E7%A9%B6%E7%BB%BC%E8%BF%B0&sc_us=11073893925633194305&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8
        }
        all_titles.append(item.get_text())
        wd = str(parse.urlparse(item.get('href')).query).split('&')[0]
        paperid = wd.split('%')[2][2:]
        params = {
            'paperid': paperid,
            'site': 'xueshu_se'
        }
        url = 'http://xueshu.baidu.com/usercenter/paper/show?' + urlencode(params)
        all_paper_urls.append(url)
        # print(url)
        # print(result)

    for abs in abstract_datas:#abs类型是<class 'bs4.element.Tag'>
        str_list = []
        for l in abs.contents:#l的类型是<class 'bs4.element.NavigableString'>
            str_list.append(str(l).replace('\n','').strip())
        # print("".join(str_list).replace('<em>','').replace('</em>',''))
        all_abstracts.append("".join(str_list).replace('<em>','').replace('</em>',''))

    for authors in author_datas:#authors类型为<class 'bs4.element.Tag'>
        for span in authors.find_all('span',limit=1):#此时span类型为<class 'bs4.element.Tag'>
            each_authors = []
            for alist in span.find_all('a'):
                each_authors.append(alist.string)
            all_authors.append(each_authors)

    return all_titles,all_authors,all_abstracts,all_paper_urls

paper = namedtuple('paper',['title','author','abstract','download_urls'])

#namedtuple()是产生具有命名字段的元组的工厂函数。命名元组赋予元组中每个位置的意义，并更易读、代码更易维护。
# 它们可以使用在通常元组使用的地方，并添加了通过名称访问字段的能力，而不是位置索引
def set_paper(all_titles,all_authors,all_abstracts,all_dlUrls):
    papers = [paper(all_titles[i],all_authors[i],all_abstracts[i],all_dlUrls[i]) for i in range(len(all_titles))]

    return papers

#获取每个文献页面的详细信息
def get_download(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None

#对于每个文献页面爬取的详细页面内容进行提取，找出所有可免费下载的地址
def get_download_urls(text):
    download_urls = []

    # pattern = re.compile('<div.*?id="savelink_wr".*?<a.*?class="dl_item".*?href="(.*?).*?<span.*?class="dl_lib".*?>(.*?)</span>.*?</div>',re.S)
    pattern = re.compile('<a.*?class="dl_item".*?href="(.*?)".*?<span.*?class="dl_lib">(.*?)</span>',re.S)
    results = re.findall(pattern,text)
    for item in results:
        each_data = {
            'url':item[0],
            'download':item[1]
        }
        if "免费" in each_data.get('download'):
            download_urls.append(each_data.get('url'))
            # print(each_data)
    return download_urls

#将文献主题、作者、摘要、下载路径转换成字典保存，使用json进行存储
def save_data(papers):
    json_papers = []
    for paper in papers:
        each_data = {
            'title':paper[0],
            'author':"/".join(paper[1]),
            'abstract':paper[2],
            'download_urls':paper[3]
        }
        json_papers.append(each_data)

    with open('baidu_xueshu.txt', 'a', encoding='utf-8') as f:
        for paper in json_papers:
            f.write(json.dumps(paper, ensure_ascii=False) + '\n')

if __name__ == '__main__':

    # -------- 程序入口处 ------------------
    print
    u"""#---------------------------------------
    #   程序：百度学术网站批量下载文献
    #   版本：1.0
    #   作者：acorn
    #   日期：2019-03-12
    #   语言：Python 3.7
    #   操作：输入关键词后爬取所有相关文献信息，将文献主题，作者，摘要，可免费下载的网址爬取下来并保存到本地文件
    #   功能：将需要查询的文献信息打包txt存储到本地。
    #---------------------------------------
    """

    # keywords = "深度学习"
    keywords = str(input("请输入在百度学术网站需要查询的关键词：\n"))
    print("开始爬取百度学术网站关于“{}”关键词的相关内容".format(keywords))
    for i in range(1):
        print("开始爬取第{}页的内容".format(str(i+1)))
        offset = i * 10
        text = get_page(keywords,offset)
        all_titles, all_authors, all_abstracts,all_paper_urls = get_urls(text)

        all_dlUrls = []
        for k in range(len(all_paper_urls)):
            new_text = get_download(all_paper_urls[k])
            download_urls = get_download_urls(new_text)
            all_dlUrls.append(download_urls)

        papers = set_paper(all_titles, all_authors, all_abstracts,all_dlUrls)
        save_data(papers)

    print("保存成功！")


