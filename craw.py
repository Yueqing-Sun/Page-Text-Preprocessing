#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import io
import sys
import time
from selenium import webdriver
import time


# 函数功能：得到今日哈工大首页所有新闻链接
def getHITurl():
    urls = ["http://today.hit.edu.cn/category/10?page={}".format(str(i)) for i in range(0, 70)]
    # driver = webdriver.Chrome('D:\Applaction\chromedriver_win32\chromedriver.exe')  # 创建一个driver用于打开网页，记得找到brew安装的chromedriver的位置，在创建driver的时候指定这个位置
    # driver.get(url)  # 打开网页

    urlset = set()
    page = 10
    for url in urls:
        wbdata = requests.get(url).text
        soup = BeautifulSoup(wbdata, 'lxml')
        news_titles = soup.select("span > span > a")
        for n in news_titles:
            link = n.get("href")
            link = "http://today.hit.edu.cn" + link
            urlset.add(link)
            print(link)

        # driver.find_element_by_xpath("//a[contains(text(),'转到下一页')]").click()  # selenium的xpath用法，找到包含“下一页”的a标签去点击
        # page = page + 1
        # time.sleep(2)  # 睡2秒让网页加载完再去读它的html代码
        print(page, "********************************")
        page = page + 1

    return urlset


# 爬取网页标题、内容、附件
def craw(allurls):
    urlset = allurls
    # print(urlset)
    i = 0
    with open('D:/news/data8.json', 'w', encoding='utf-8') as ff:
        for url in urlset:
            try:
                time.sleep(2)
                print("url: ", url)
                data = urllib.request.urlopen(url).read()
                data2 = data.decode("utf-8", "ignore").replace(u'\xa9', u'').replace(u'\xa0', u'')

                soup = BeautifulSoup(data2, "lxml")

                title = soup.select('h3')  # 如果标题不存在，跳过
                if len(title) == 0:
                    print("ERROR: 没有标题")
                    continue

                content = soup.select('p')
                text = ""
                for m in range(0, len(content)):
                    con = content[m].get_text().strip()
                    if (len(con) != 0):
                        text = text + con

                    m += 1
                if len(text) < 50:  # 如果文本太短，跳过
                    print("ERROR: 文本太短")
                    continue
                print("title: ", title[0].get_text().strip())
                print("text: ", text)

                file_urls = soup.find_all('span', {"class": "file--x-office-document"})
                print("file_ul: ", file_urls)
                names = []
                if len(file_urls):
                    for item in file_urls:
                        file = item.select('a')
                        print("file: ", file)
                        file_name = file[0].get_text().strip()  # 文件名
                        names.append(file_name)
                        print("file_name: ", file_name)
                        fileurl = file[0].get('href')  # 文件的链接
                        print("fileurl: ", fileurl)
                        r = requests.get(fileurl, stream=True)

                        with open('D:/news/file_new/%s' % file_name, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=128):
                                f.write(chunk)
                        print('Saved %s' % file_name)
                data = {
                    "url": url,
                    "title": title[0].get_text().strip(),
                    "parapraghs": text,
                    "file_name": names
                }
                json_str = json.dumps(data, ensure_ascii=False)
                ff.write(json_str + '\n')
                print("count: ", i)
                i = i + 1

            except Exception as err:
                print(err)


# 单个链接的测试程序，可忽略
def craw2():
    url = "http://today.hit.edu.cn/article/2019/04/23/66252"
    data = urllib.request.urlopen(url).read()
    data2 = data.decode("utf-8", "ignore").replace(u'\xa9', u'')

    soup = BeautifulSoup(data2, "lxml")
    title_ul = soup.find_all('div', {"class": "article-title text-center"})
    print("title_ul: ", title_ul[0].get_text().strip())
    content = soup.select('p')
    title = soup.select('h3')
    print("title: ", title)
    print(title[0].get_text().strip())
    text = ""
    for m in range(0, len(content)):
        con = content[m].get_text().strip()
        if (len(con) != 0):
            text = text + con
        m += 1
    print(text)

    file_ul = soup.find_all('span', {"class": "file--x-office-document"})
    print("file_ul:", file_ul)
    names = []
    for ul in file_ul:
        imgs = ul.select('a')
        print("imgs: ", imgs)
        image_name = imgs[0].get_text().strip()
        print("image_name: ", image_name)
        names.append(image_name)
        fileurl = imgs[0].get('href')
        print("fileurl: ", fileurl)
        r = requests.get(fileurl, stream=True)

        with open('./img/%s' % image_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s' % image_name)
    # with open('D:/news/data4.json', 'w') as f:
    #     data = {
    #         'url': url,
    #         'title': title[0].get_text().strip(),
    #         'parapraghs': text,
    #         'file_name': names
    #     }
    #     json_str = json.dumps(data, indent=4, ensure_ascii=False)
    #     f.write(json_str)
    #     f.write("\n")


if __name__ == '__main__':
    start = time.time()
    allurls = getHITurl()
    craw(allurls)
    # craw2()
    end = time.time()
    print('Total time: %.1f s' % (end - start,))
