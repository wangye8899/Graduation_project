import requests
import pymongo
from bs4 import BeautifulSoup
from lxml import etree
import  random
import re
import time
import json

movie_detail={
    # 'movie_name':
    # 
}
headers = [

        {"user-agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        #火狐
        {"user-agent" : "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        #谷歌
        {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]

# 数据库的链接操作，并将集合返回
def connect_mongo():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.douban
    collection = db.movie
    # collection = db.back_up
    return collection
def short_comment_process(url):
    # 开始爬评价
    html = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(html.content.decode('utf-8'))
    # span_list = tree.xpath('//span[@class="comment-info"]')
    # for span in 
    # comment_score = re.findall(r"\d+\.?\d*",str(comment_score))[0]
    # movie_detail['comment_score'] = comment_score
    div_list = tree.xpath('//div[@class="comment"]')
    for div in div_list:
        comment_info = div.xpath('./p/span/text()')
        comment_score = div.xpath('./h3/span[@class="comment-info"]/span[2]/@class')
        comment_score = re.findall(r"\d+\.?\d*",str(comment_score))[0]
        movie_detail['comment_info'] = comment_info
        movie_detail['comment_score'] = comment_score
        print(movie_detail)
        collection = connect_mongo()    
        try:
            if collection.insert({'movie_name':movie_detail['movie_name'],'movie_score':movie_detail['movie_score'],'comment_info':movie_detail['comment_info'],'comment_score':movie_detail['comment_score']}):
                print('成功存入数据库')
        except pymongo.errors.DuplicateKeyError:
                # 对唯一字段进行重复插入，pymongo则会抛出这个错误，并且插入失败
            print("重复插入")
            pass
def detail_process(url):
    html = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(html.content.decode('utf-8'))
    short_comment_url = tree.xpath('//div[@id="comments-section"]/div[1]/h2/span/a/@href')[0]
    # ['https://movie.douban.com/subject/26752088/comments?status=P'
    # https://movie.douban.com/subject/26752088/comments?start=0&limit=20&sort=new_score&status=P&percent_type=h
    short_comment_hurl = short_comment_url.split('?')[0]+'?start=0&limit=20&sort=new_score&status=P&percent_type=h'
    short_comment_lurl = short_comment_url.split('?')[0]+'?start=0&limit=20&sort=new_score&status=P&percent_type=l'
    movie_detail['movie_score'] = tree.xpath('//strong[@class="ll rating_num"]/text()')
    short_comment_process(short_comment_hurl)
    short_comment_process(short_comment_lurl)
    # print(html.content.decode('utf-8'))
    # print(short_comment_url)
def movie_process(url):
    response = requests.get(url,headers=random.choice(headers))
    response = response.json()
    info = response['subjects']
    for m in range(0,19):
        movie_name = info[m]['title']
        movie_url = info[m]['url']
        movie_detail['movie_name'] = movie_name
        detail_process(movie_url)


def allmovie_process():
    # for循环构造所有电影的链接
    for i in range(0,15):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=recommend&page_limit=20&page_start='+str(i*20)
        movie_process(url)


allmovie_process()

