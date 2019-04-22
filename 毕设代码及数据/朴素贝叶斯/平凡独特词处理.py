from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import jieba
import csv
import pandas as pd

global wordslist,scorelist
wordslist = []
scorelist = []
def ReadMongo():
    """
    函数说明：读取mongodb数据 然后进行预处理 使用正则 beautifulsoup等工具 具体思路就是清洗数据 去掉英文 字符 表情 然后根据评论的星数打上标签1 2星标0 4 5星标1 
    """
    global wordslist,scorelist
    comment_score=[]
    stri=""
    summ=0
    comment={}
    allcommentwords = []
    connect = MongoClient('localhost',27017)
    db = connect.douban
    # f = open('训练集.txt','a+')
    # fp = open('影评训练.csv','a+')
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # print(list(db.movie.find().limit(20)))
    for info in db.movie.find().limit(1000):
        if len(info['comment_info']):
            info['comment_info'] = str(info['comment_info'][0]).strip()
            info['comment_info'] = str(BeautifulSoup(info['comment_info'],"html.parser"))
            # 使用BeautifulSoup去除所有html标签
            info['comment_info'] = str(re.sub(r1,'',info['comment_info']))
            emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            #    u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
            info['comment_info'] = str(emoji_pattern.sub(r'',info['comment_info']))
            info['comment_info'] = info['comment_info'].replace("\n","")
            info['comment_info'] = ''.join(info['comment_info'].split())
            info['comment_info'] = jieba.cut(info['comment_info'],cut_all = False)
            info['comment_info'] = " ".join(info['comment_info'])
            # print(info['comment_info'])
            info['comment_info'] = Stopwords_process(info['comment_info'])
            comment['comment_info'] = info['comment_info']
            for i in comment['comment_info'].split(" "):
                if len(i):
                    wordslist.append(i)
                else:
                    pass
            wordslist.append("$")
            # wordslist.remove(wordslist[-1])
            info['comment_score'] = int(info['comment_score'])/10
            # 此处直接根据电影评价的评分打标签 因为 3分作为分界点 1 2 均为消极情感 4 5 为积极情感 
            if info['comment_score'] == 1:
                info['comment_score']= 0
                comment['comment_score'] = info['comment_score']
                scorelist.append(info['comment_score'])
               
            elif info['comment_score'] == 2:
                info['comment_score']= 0
                comment['comment_score'] = info['comment_score']
                scorelist.append(info['comment_score'])
            else :
                info['comment_score'] = 1
                scorelist.append(info['comment_score'])
                comment['comment_score'] = info['comment_score']
            if len(info['comment_info']):
                pass
                # stri+=str(comment_score)+" "+ comment_info+"wangye"
                # f.write(str(info['comment_score'])+" "+ info['comment_info']+"\n") 
                # w = csv.DictWriter(fp,comment.keys())
                # w.writerow(comment)
            else:
                pass
        else:
            pass
    # f.close()
    print(wordslist)
    print(len(scorelist))
    Frequence_process(wordslist,scorelist)

def Frequence_process(wordlist,scorelist):
    """
    函数说明：词频处理
    参数说明：
        wordlist：所有单词构成的列表
        scorelist：0,1列表
    思路：将频占比0.8和词频小于5的词语剔除
    """
    newwordslist=[]
    newwordslist2=[]
    print("词频处理中。。。。。。。。。。。。。。。。。。。。。。。。")
    for word in wordslist:
        if wordslist.count(word)/len(wordslist)>0.8:
            # if word !='$':
            #     wordslist.remove(word)
            #     print(word)
            if word=='$':
                newwordslist.append(word)
        else:
            # 过滤到单个字        
            newwordslist.append(word)

    for word1 in newwordslist:
        if newwordslist.count(word1)<6:
            if word1=='$':
                newwordslist2.append(word1)
        else:
            newwordslist2.append(word1)
    print("未处理前的词语数")
    print(len(wordlist))
    print("两次降低维度处理")
    print("处理后的词语数")
    print(len(newwordslist2))
    print(newwordslist2)
    print("字符串分割成list处理")
    # 对list中的元素 使用空格相连 根据$ 进行分割 逐行写入txt
    wordstr = " ".join(i for i in newwordslist2)    
    sublist = wordstr.split('$')
    print(sublist)
    sublist.remove(sublist[-1])
 
    fw = open('训练集.txt','a+')
    fp = open('对比训练集.txt','a+')
    fp.writelines(wordlist)
    for i in range(len(sublist)):
        if len(sublist[i])!=1:
            if len(sublist[i])==0:
                pass
            else:
                fw.write(str(scorelist[i])+" "+str(sublist[i])+"\n")
        
    print("数据预处理完毕")
    fw.close()

def Stopwords_process(str):
    """
    函数说明：停用词处理
    str：传进来的每一句评论数据
    """
    # print(str)
    global wordslist,scorelist
    n = 0
    print("***********************************************************************************")
    stopwords = [line.strip() for line in open('哈工大停用词表.txt','r',encoding='utf-8').readlines()]  
    outstr=""
    for oneword in str:
        if oneword not in  stopwords:
            outstr+=oneword
            outstr+=""
            n+=1  
    print("停用词处理")
    print(outstr)
    return outstr
    
def More_process():
    """
    函数说明：对词频处理后的训练集再进行词频统计 然后按词频高低取前八个
    未进行
    """
ReadMongo()