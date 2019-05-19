import requests
import pymongo
from bs4 import BeautifulSoup
from lxml import etree
import  random
import re
import time
import json

global data 
data = 0
headers = [

        {"user-agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        #火狐
        {"user-agent" : "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        #谷歌
        {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]

def music_process(url,string):
    pic_url = []
    music_info = []
    response = requests.get(url,headers=random.choice(headers))
    tree = etree.HTML(response.content.decode('utf-8'))
    table_list  = tree.xpath('//div[@id="subject_list"]/table')
    for table in table_list:
        link = table.xpath('./tr/td[1]/a/img/@src')
        pic_url.append(link[0])
        music = table.xpath('./tr/td[1]/a/img/@alt')[0]
        music_info.append(music)
    Write_to_file(pic_url,music_info,string)

    # 制作链接
   
    
def Write_to_file(pic_url,music_info,string):
    global data
    p = re.compile(r'[\u4e00-\u9fa5]')
   
    for i in range(len(pic_url)):
        img = requests.get(str(pic_url[i]))
        music_name = re.findall(p,str(music_info[i]))
        
        fw = open('/home/wangye/'+str(string)+'/'+str(''.join(music_name))+'.jpg','wb+')
        fw.write(img.content)
        # time.sleep(1)
        print("该图片"+str(music_info[i]+"被写入文件夹"))
        data +=1
        if data%10 == 0 :
            print("已经写入"+str(data)+"张")


# cate_proess('https://music.douban.com/tag/')
if __name__ == "__main__":


    # for i in range(24):
     
    #     num = i*20
    #     next_page_url = "https://music.douban.com/tag/中国?start="+str(num)+"&type=T"
    #     music_process(next_page_url,"IMG1")
    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/粤语?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG2")

    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/日本?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG3")

    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/韩国?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG4")

    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/英国?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG5")
        

    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/民谣?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG6")
        

    # for i in range(24):
    #     num = i*20
    #     next_page_url1 = "https://music.douban.com/tag/流行?start="+str(num)+"&type=T"
    #     music_process(next_page_url1,"IMG7")
        
    for i in range(24):
        num = i*20
        next_page_url1 = "https://music.douban.com/tag/摇滚?start="+str(num)+"&type=T"
        music_process(next_page_url1,"IMG8")  

    for i in range(24):
        num = i*20
        next_page_url1 = "https://music.douban.com/tag/pop?start="+str(num)+"&type=T"
        music_process(next_page_url1,"IMG9")  

    for i in range(24):
        num = i*20
        next_page_url1 = "https://music.douban.com/tag/电子?start="+str(num)+"&type=T"
        music_process(next_page_url1,"IMG10")  
        
         