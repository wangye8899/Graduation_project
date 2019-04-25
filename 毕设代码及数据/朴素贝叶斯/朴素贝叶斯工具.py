from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import jieba
import pkuseg
import csv 
import pandas as pd
import gc
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB




def Comments_process(wy):
    scorelist = []
    wordslist = []
    """
    函数说明： 读mongo数据库，将评论数据生成list，返回CountVector/TFIDFVector使用
    wy：数据库读取数目，0代表全部读取                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    """

    connect = MongoClient('localhost',27017)
    db = connect.douban
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

    # 判断数据库读取条数
    if wy ==0:
        dbdata = db.movie.find()
    else:
        dbdata = db.movie.find().limit(wy)
    
    for info in dbdata:
        # 仅处理评论不为空的情况
        if len(info['comment_info']):
            # 正则表达式、BeautifulSoup处理
            info['comment_info'] = ReHtml_process(str(info['comment_info'][0]))
            # jieba分词处理
            info['comment_info'] = Jieba_process(str(info['comment_info'])) 
            # pkuseg分词处理
            # info['comment_info'] = pkuseg_process(str(info['comment_info']))
            # 处理评论分数
            info['comment_score'] = Score_process(info['comment_score'])
            scorelist.append(info['comment_score'])
            wordslist.append(info['comment_info'])
    
    return wordslist,scorelist


def CommonFeature(wordslist):
    """
    处理评论文本中过于平凡的词和过于独特的词
    """          
    with open('哈工大停用词表.txt','rb') as fp:
        stopword = fp.read().decode('utf-8')
    stopwordslist = stopword.splitlines()
    vect=TfidfVectorizer(binary=False,decode_error='ignore',max_df=0.8,min_df=10,stop_words=stopwordslist)
    # vect = CountVectorizer(max_df=0.8,min_df=3,stop_words=stopwordslist)
    vect_fro = CountVectorizer()
    comment_vec = vect.fit_transform(wordslist).toarray()
    print("共有评论文本数据%s"%len(comment_vec)+"条")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    # 使用pandas工具统计特征数

    front = pd.DataFrame(vect_fro.fit_transform(wordslist).toarray(),columns=vect_fro.get_feature_names())
    MaxMin = pd.DataFrame(vect.fit_transform(wordslist).toarray(),columns=vect.get_feature_names())
    print("未去除停用词之前的特征数为%s"%front.shape[1])
    print("去除停用词、平凡词和特征词后的特征总数为：%s"%MaxMin.shape[1])
    return comment_vec
    

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
def pkuseg_process(infostr):
    # 去除空格，连接成一句话。
    stopstr = ''.join(infostr.split())
    seg = pkuseg.pkuseg()
    text = seg.cut(stopstr)
    print(text)
    # stopstr = ' '.join(stopstr)
    # print(stopstr)
    return stopstr

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


if __name__ == "__main__":
    wordslist,scorelist =Comments_process(5000)
    comment_vec = CommonFeature(wordslist)
    comment_train,comment_test,target_train,target_test = train_test_split(comment_vec,scorelist,test_size = 0.25,random_state = 0)  
    wyNB = MultinomialNB()
    # wyNB = BernoulliNB()
    wyNB.fit(comment_train,target_train)
    acc = wyNB.score(comment_test,target_test)
    print(acc) 