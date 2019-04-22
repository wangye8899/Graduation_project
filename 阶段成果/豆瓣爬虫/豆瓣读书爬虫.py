import requests
import pymongo
from bs4 import BeautifulSoup
from lxml import etree
import  random
import re
import time
import json
book_detail = {
    # 'category':
    # 'book_name':
    # 'book_score':
    # 'comment_score':
    # 'author':
    # 'comment':response.json()['html']
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
    collection = db.book
    return collection
def comment_get(url):
    
    response = requests.get(url,headers=random.choice(headers))
    content = re.split(r'\s+',response.json()['html'])
    dr = re.compile(r'<[^>]+>',re.S)
    comment = dr.sub('',''.join(content))
    book_detail['book_comment'] = comment
    print(book_detail)
    collections = connect_mongo()
    try:
        if collections.insert({'category':book_detail['category'],'book_name':book_detail['book_name'],'book_score':book_detail['book_score'],'comment_score':book_detail['comment_score'],'comment':book_detail['book_comment']}):
             print('成功存入数据库')
    except pymongo.errors.DuplicateKeyError:

         # 对唯一字段进行重复插入，pymongo则会抛出这个错误，并且插入失败
        print("重复插入")
        pass
    

def comment_process(url,score,name):
   
    book_detail['comment_score'] = score
    # print(book_detail['comment_score'])
    print(url)
    html = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(html.content.decode('utf-8'))
    div_list= tree.xpath('//div[@class="main review-item"]')
    if div_list:
        for div in div_list:
            url = 'https://book.douban.com/j/review/'+div.xpath('@id')[0]+'/full'
            print(url)
            print(div.xpath('@id')[0])
            print(score)
            comment_get(url)
        
    else:
        print(name+'没有'+str(score)+'评价')
        print('链接为'+url)
       
        

       

    
def score_process(url,name):
    print(url)
    time.sleep(1)
    html = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(html.content.decode('utf-8'))
    book_detail['author'] = tree.xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[2]/a[1]/text()')
    # print(book_detail['author'])
    # 构造评分链接

    url_rating5 = url+'reviews?'+'rating=5'
    url_rating4 = url+'reviews?'+'rating=4'
    url_rating1 = url+'reviews?'+'rating=1'
    url_rating2 = url+'reviews?'+'rating=2'
    
    comment_process(url_rating1,1,name)
    comment_process(url_rating2,2,name)
    comment_process(url_rating4,4,name)
    comment_process(url_rating5,5,name)
    
def booklist_process(param):
    # 由于链接的规律性 故直接构造url 且每类只爬1页 20本书
    # for num in range(0,10):
        # num = num*20
    time.sleep(1)
    url = 'https://book.douban.com/tag/'+param+'?'+'start='+str(0)
    
    html = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(html.content.decode('utf-8'))
    li_list = tree.xpath('//ul[@class="subject-list"]/li')
    for li in li_list:
        url = li.xpath('./div[@class="info"]/h2/a/@href')[0]
        bookname = li.xpath('./div[@class="info"]/h2/a/text()')
        # print(bookname)
        book_detail['book_name'] =re.split(r'\s+',bookname[0])[1]
        book_detail['book_score'] =  li.xpath('./div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
        # print(book_detail['book_name'])
        # print(book_detail['book_score'])
        # print(re.split(r'\s+',bookname[0])[1])
        # print(url)
        score_process(url,book_detail['book_name'] )

def catagory_process(url):
    
    html = requests.get(url,headers=random.choice(headers))
    print(html)
    tree = etree.HTML(html.content.decode('utf-8'))
    # 通过xpath 拿到类别的url 
    table_list = tree.xpath('//table[@class="tagCol"]')
    # 共五个板块table 依次循环 取值
    
    for table in table_list:
        tr_list = table.xpath('./tbody/tr')
        for tr in tr_list:
            td_list = tr.xpath('./td')
            for td in td_list:
                temp_url = td.xpath('./a/@href')
                # 拼接成每个类别的url
                category_url = 'https://book.douban.com'+temp_url[0]
                book_detail['category'] = td.xpath('./a/text()')
                print(td.xpath('./a/text()')[0])
                booklist_process(td.xpath('./a/text()')[0])

catagory_process("https://book.douban.com/tag/?view=type&icn=index-sorttags-all")
