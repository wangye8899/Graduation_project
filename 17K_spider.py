import requests
import pymongo
from bs4 import BeautifulSoup
from lxml import etree
import  random
global First_classify,SecondClassify

# 数据库操作代码
def connect_mongo():
    global First_classify,SecondClassify
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.story
    collection = db.name
    return collection
def insertMongo(FirstClassify,SecondClassify,storyname,collection):
    global First_classify,SecondClassify
    collection = connect_mongo()    
    try:
        if collection.insert({'FirstClassify':FirstClassify,'SecondClassify':SecondClassify,'storyname':storyname}):
            print('成功存入数据库')
    except pymongo.errors.DuplicateKeyError:
            # 对唯一字段进行重复插入，pymongo则会抛出这个错误，并且插入失败
        print("重复插入")
        pass

def process(url):
    global First_classify,SecondClassify
    First_classify=""
    second_list = []
    second_url = []
    response = requests.get(url)
    tree = etree.HTML(response.content.decode('utf-8'))
    First_classify = tree.xpath('//a[@class="on fb"]/text()')[0]
    p_list = tree.xpath('//div[@class="fllist-item"]/dl/dd[3]/p')
    for item in p_list:
        second_list = item.xpath('./a/text()')
        second_url = item.xpath('./a/@href')
    # print(second_list)
    # print(second_url)
    for i in range(len(second_url)):
        strurl = "http://all.17k.com"+str(second_url[i])
        print("第一类别名："+str(First_classify))
        print("第二类别名"+str(second_list[i]))
        process_details(strurl,str(First_classify),str(second_list[i]))
        
def process_details(strurl,fir,str):
    
    headers = [

        {"user-agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        #火狐
        {"user-agent" : "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        #谷歌
        {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]
    res = requests.get(strurl,headers=random.choice(headers))
    tree = etree.HTML(res.content.decode('utf-8')) 
    # print(res.content.decode('utf-8'))  
    tr_list = tree.xpath('//a[@class="jt"]/text()')
    print("对应书名如下")
    print(tr_list[1:6])
    story_name = ''.join(tr_list[1:6])
    # 链接mongoDB数据库
    collection = connect_mongo()
    # 插入数据库
    insertMongo(fir,str,story_name,collection)
if __name__ == "__main__":
    url1 = "http://all.17k.com/lib/book/2_21_0_0_0_0_0_0_1.html"
    url2 = "http://all.17k.com/lib/book/2_24_0_0_0_0_0_0_1.html"
    url3 = "http://all.17k.com/lib/book/2_3_0_0_0_0_0_0_1.html"
    url4 = "http://all.17k.com/lib/book/2_22_0_0_0_0_0_0_1.html"

    # url2
    process(url1)
    process(url2)
    process(url3)
    process(url4)