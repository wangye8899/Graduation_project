import jieba
from pymongo import MongoClient
import csv
import re
# def DBConnect():

def Movie_process():
    connect = MongoClient('localhost',27017)
    db = connect.douban
    for info in db.movie.find():
        print(info['comment_info'])
        if len(info['comment_info']):
            comment_info = str(info['comment_info'][0]).strip()
            info['comment_info'] = comment_info.replace(' & nbsp',"") 
            # print(info['comment_info'])
            seg_list = jieba.cut(str(info['comment_info']))
            # print(" ".join(seg_list))
            info['comment_info'] = " ".join(seg_list)
            # 将分词后的句子 进行停用词过滤
            info['comment_info'] = StopWords_process(info['comment_info'])
            info['comment_score'] = int(info['comment_score'])/10
            info['movie_score'] = info['movie_score'][0]
            # print(info)
            f = open ('豆瓣影评评论.txt',"a+")
            f.write(info["comment_info"]+"   "+str(info["comment_score"])+"\n")
            fp = open('豆瓣影评.csv',"a+")
            w = csv.DictWriter(fp,info.keys())
            w.writerow(info)

        else:
            print("字段被抛弃")
    f.close()  
    fp.close()
    connect.close()
   
def Book_process():
    connect = MongoClient('localhost',27017)
    db = connect.douban
    for book in db.book.find():
        comment = str(book['comment'])
        comment.strip()
        comment = comment.replace('&nbsp;',"")
        book['comment'] = comment
        # print(book['comment'])
        seg_list = jieba.cut(str(book['comment']))
        book['comment'] = " ".join(seg_list)
        book['comment'] = StopWords_process(book['comment'])
        book['category'] = str(book['category'][0])
        book['book_score'] = book['book_score'][0]
        # print(book)
        f = open('豆瓣书评.csv',"a+")
        w = csv.DictWriter(f,book.keys())
        w.writerow(book)
        ftxt = open('豆瓣书评.txt',"a+")
        ftxt.write(book["comment"]+" "+str(book["comment_score"])+"\n")
    
    f.close()
    ftxt.close()
    connect.close()

# 处理停用词 进行过滤 

# def StopWords_process(str):
    # fp = open(str,"r+",encoding='utf-8')
    # stwords_list = []
    # f = open('../stopwords/哈工大停用词表.txt',"r",encoding='utf-8')
    # for line in f :
    #     stwords_list.append(list(line.strip('\n').split(',')))
    # for line in fp:
    #     print(line)
    #     for sw in stwords_list:
    #         print(sw[0])
    #         if sw[0] in line:
    #             s = line.replace(sw[0],"")
    #             print(line)
    #     #         fp.writelines(s)
    #     #         print("已经替换掉"+sw[0])
        
    # fp.close()
    # f.close()



def StopWords_process(seg_words):
    print(seg_words)
    print("***********************************************************************************")
    stopwords = [line.strip() for line in open('../stopwords/stopwords/哈工大停用词表.txt','r',encoding='utf-8').readlines()]  
    outstr=""
    for oneword in seg_words:
        if oneword not in  stopwords:
            outstr+=oneword
            outstr+=""
    
    print("去除停用词"+outstr)
    return outstr
    
Movie_process()
Book_process()     
