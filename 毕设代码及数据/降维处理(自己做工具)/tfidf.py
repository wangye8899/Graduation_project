from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import jieba
import csv 
import pandas as pd
import gc
import numpy as np

global wordslist,scorelist,lines
lines = 0
wordslist = []
scorelist = []
filename = '未TFIDF数据集.txt'
def Comments_proccess(wy,filename):
    global scorelist
    """
    函数说明：读Mongo然后做初步处理
    """
    fw = open(filename,'a+')
    connect = MongoClient('localhost',27017)
    db = connect.douban
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # 评论个数

    global lines 
    num = 0
    if wy == 0:
        dbdata = db.movie.find()
    else:
        dbdata = db.movie.find().limit(wy)
    for info in dbdata:

        if len(info['comment_info']):
        #  当评论数据不为空的时候处理
        # 正则。Beautifulsoup处理
            # print("未处理"+str(info['comment_info'][0]))
            info['comment_info'] = ReHtml_process(str(info["comment_info"][0]))
            # jieba分词处理
            info['comment_info'] = Jieba_process(str(info['comment_info']))
            # 停用词处理
            info['comment_info'],wordslist = Stopwords_process(str(info['comment_info']),'哈工大停用词表.txt')
            wordslist = More_process(wordslist)
            # print("处理完"+info['comment_info'])
            # 处理分数
            info['comment_score'] = Score_process(info['comment_score'])
            scorelist.append(info['comment_score'])
            if len(wordslist):
                fw.write(str(info['comment_score'])+"$"+info['comment_info']+"\n")
                lines+=1
                # else:
                #     print("目前不可以操作"+str(num))
            num+=1

    fw.close()
# 通过临时写文件转存数据
# 调用函数开始求解
    

def StratTFIDF(filename,lenofword,sumofcomment):
    global scorelist
    fr = open(filename,'r')
    newwords=[]
    Processed_Words=[]
    comment=""
    # 计算每个词的tf—idf
    i=0

    # 原写法
    for line in fr.readlines():
        onecomment_list = line.split('$')[1].split(' ')
        wordslist = More_process(onecomment_list)
        FinalTfIdf = TF_IDF_process(wordslist,sumofcomment,filename)
        # tfidf 最大的前八个词   
        Processed_Words = MaxThreeWords(wordslist,FinalTfIdf,lenofword)
        comment = ListToString(Processed_Words)
        print(comment)
        fwrite = open('TFIDF数据3.txt','a+')
        fwrite.write(str(line.split('$')[0])+' '+str(comment)+"\n")
        # fwrite.write(str(scorelist[i])+"$"+str(comment)+"\n")
        i+=1
        print("处理数据数量")
        print(i)
    fwrite.close()    
    fr.close()

def Score_process(comment_score):

    comment_score = int(comment_score)/10
            # 此处直接根据电影评价的评分打标签 因为 3分作为分界点 1 2 均为消极情感 4 5 为积极情感 
    if comment_score == 1:
        comment_score= 0

    elif comment_score == 2:
        comment_score = 0
    else :
        comment_score = 1

    return comment_score
def ReHtml_process(infostr):
    """
    去除字符串中非中文部分
    """
    newstr = str(infostr.replace("\n",""))
    newstr = str(BeautifulSoup(infostr.strip(),"html.parser"))
    # 定义两个正则匹配
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            #    u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)

    # 正则处理，表情、符号、图标、英文字符
    newstr = str(re.sub(r1,'',newstr))
    newstr = str(emoji_pattern.sub(r'',newstr))
    return newstr
def Jieba_process(infostr):
    # 出去空格，链接成一句话，无论是否通顺
    stopstr = ''.join(infostr.split())
    stopstr = jieba.cut(stopstr,cut_all=False)
    stopstr = ' '.join(stopstr)
    return stopstr
def Stopwords_process(infostr,stopwordspath):
    """
    去除停用词
    """
    wordslist=[]
    stopwords = [line.strip() for line in open(stopwordspath,'r',encoding='utf-8').readlines()] 
    outstr=""
    for word in infostr:
        if word not in stopwords:
            wordslist.append(word)
            outstr+=word
            # outstr+=""
    return outstr,wordslist
def More_process(wordslist):
    newwords_list=[]
    for item in wordslist:
        if len(item) == 0:
            continue
        else:
            newwords_list.append(item)

    return newwords_list
def TF_IDF_process(wordslist,lines,filename):
    """
    应用TF*IDF算法 找出一句评论中，最能代表这句话感情色彩的几个词，从而达到优化算法，降低维度的作用
    """
    # 声明字典
    TfIdf_list = []
    max_frequence=0
    # 统计最大词频
    for word in wordslist:
        if wordslist.count(word) > max_frequence:
            max_frequence = wordslist.count(word)
    # 统计每个词的词频 公式：词频数 = 单个词频 / 最大频数
    for i  in range(len(wordslist)):
        # print(tem)
        TfIdf_Dic = {}
        TfIdf_Dic['word'] = str(wordslist[i])
        # 词频数 = 单个词频 / 最大频数
        TfIdf_Dic['frequence'] = wordslist.count(wordslist[i])/max_frequence
        TfIdf_list.append(TfIdf_Dic)
    # print(TfIdf_list)
    # 下面计算每个词的IDF
    # 读文件 将所有评论存入列表
    all_comment_list=[]
    fmr = open(filename,'r')
    for line in fmr.readlines():
        comment_str = str(line.split('$')[1])
        all_comment_list.append(comment_str)   

    # 循环列表，统计IDF值
    idf=0
    TfIdf=[]
    lines = 23553
    for dic in TfIdf_list:
        for sent in all_comment_list:
            if str(dic['word']) in str(sent):
                idf+=1 
        # 已经算完了包含当前单词的文档总数，那么计算每个词tfidf值
        TfIdf.append(np.log(lines/idf+1))
        idf =0

    # 计算tf*idf
    FinalWordsTfIdf={}
    FinalTfIdf = []
    templist=[]

    for i in range(len(TfIdf_list)):
        tfidf = float(TfIdf[i])*float(TfIdf_list[i]['frequence'])
        FinalTfIdf.append(tfidf)
    return FinalTfIdf
def MaxThreeWords(wordslist,tfidflist,n):
    """
    拿到词汇序列中的idf最大的前n个词汇
    """
    # 先去掉重复的单词，以及其对应的tfidf值
    return_words_list=[]
    tempwordlist = []
    temp_tfidf_list = []
    for i in range(len(wordslist)):
        if wordslist[i] not in tempwordlist:
            tempwordlist.append(wordslist[i])
            temp_tfidf_list.append(tfidflist[i])
        else:
            continue
    
    maxtd = 0
    temp = 0
    num = 0
    print(temp_tfidf_list)
    print(tempwordlist)
    if n>len(tempwordlist):
        return tempwordlist
    while num!=n:
        for a in range(len(tempwordlist)):
            if temp_tfidf_list[a]>=maxtd:
                maxtd = temp_tfidf_list[a]
                temp = a
            else:
                continue
        maxtd=0
        # print(temp_tfidf_list[temp])
        #循环结束之后，拿到最大值，还有最大值对应的下标
        return_words_list.append(tempwordlist[temp])
        tempwordlist.remove(tempwordlist[temp])
        temp_tfidf_list.remove(temp_tfidf_list[temp])
        num+=1

    print(return_words_list)
    Sum(return_words_list)
    return return_words_list
def ListToString(wordlist):
    comment = ' '.join(wordlist)
    comment = comment.replace("\n","")
    print(comment)
    return comment
def Sum(wordslist):
    # 使用set的数据结构 去除重复的词汇
    vocabList = set([])
    for doc in wordslist :
        vocabList = vocabList | set(doc) 
    # 以列表的形式返回 不重复词汇的集合
    print("TFIDF处理后的总特征数："+str(len(vocabList)))
    # return list(vocabList)

if __name__ == "__main__":

    # filename = '未TFIDF数据集.txt'
    # Comments_proccess(0,filename)
    filename = '平凡独特训练集.txt'
    StratTFIDF(filename,3,lines)