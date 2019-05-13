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
from sklearn.naive_bayes import GaussianNB
import sys 
sys.path.append('../降维处理(自己做工具)/词性标注')
import 词性标注 as wordpro
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer





def Comments_process(wy):
    scorelist = []
    wordslist = []
    fw = open('全部数据.txt','a+')
    """
    函数说明： 读mongo数据库，将评论数据生成list，返回CountVector/TFIDFVector使用
    wy：数据库读取数目，0代表全部读取                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    """

    connect = MongoClient('localhost',27017)
    db = connect.douban
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    sence = []
    # 判断数据库读取条数
    if wy ==0:
        dbdata = db.movie.find()
    else:
        dbdata = db.movie.find().limit(wy)
    
    for info in dbdata:
        # 仅处理评论不为空的情况
        if len(info['comment_info']):
            if count(str(info['comment_info']),sence):                          
                # 正则表达式、BeautifulSoup处理
                info['comment_info'] = ReHtml_process(str(info['comment_info'][0]))
                # 去除停用词
                info['comment_info'] = Stopwords_process(str(info['comment_info'])) 
                # pkuseg分词处理
                # info['comment_info'] = pkuseg_process(str(info['comment_info']))
                # 处理评论分数
                info['comment_score'] = Score_process(info['comment_score'])
                if len(info['comment_score']):
                    # fw.write(str(info['comment_score'])+"    "+info['comment_info']+"\n")
                    scorelist.append(info['comment_score'])
                    wordslist.append(info['comment_info'])
                else:
                    pass
    # fw.close()

    print(len(sence))
    print(len(wordslist))
    
    return wordslist,scorelist

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

def count(sentence,sence):
    if sentence not in sence:
        sence.append(sentence)
        return 1
    else:
        return 0
    # print(len(sence))

def CommonFeature(wordslist):
    """
    处理评论文本中过于平凡的词和过于独特的词
    """          
    with open('哈工大停用词表.txt','rb') as fp:
        stopword = fp.read().decode('utf-8')
    stopwordslist = stopword.splitlines()
    vect=TfidfVectorizer(binary=False,decode_error='ignore',max_df=0.8,min_df=8,stop_words=stopwordslist)
    # vect = CountVectorizer(stop_words=stopwordslist)
    # vect_fro = CountVectorizer()
    comment_vec = vect.fit_transform(wordslist).toarray()
    print("共有评论文本数据%s"%len(comment_vec)+"条")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    # 使用pandas工具统计特征数
    # front = pd.DataFrame(vect_fro.fit_transform(wordslist).toarray(),columns=vect_fro.get_feature_names())
    MaxMin = pd.DataFrame(vect.fit_transform(wordslist).toarray(),columns=vect.get_feature_names())
    # print("未去除停用词之前的特征数为%s"%front.shape[1])
    print("去除停用词、平凡词和特征词后的特征总数为：%s"%MaxMin.shape[1])
    return comment_vec
    

def ReHtml_process(infostr):
    """
    去除字符串中非中文部分
    """
    # newstr = infostr.strip()
    newstr = str(infostr.replace("\n"," "))
    newstr = str(infostr.replace("\r"," "))
    newstr = str(BeautifulSoup(newstr.strip(),"html.parser"))
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
        # comment_score= 0
        comment_score = "消极"

    elif comment_score == 2:
        # comment_score = 0
        comment_score = "消极"
    else :
        # comment_score = 1
        comment_score = "积极"

    return comment_score

def Overfitting(datasets,labelsets):
    
    # 绘制学习曲线、判断拟合情况如何
    # train_sizes,train_score,test_score = learning_curve(MultinomialNB(),datasets,labelsets,train_sizes=[0.1,0.2,0.4,0.6,0.8,1],cv=10,scoring='accuracy')
    # train_sizes,train_score,test_score = learning_curve(GaussianNB(),datasets,labelsets,train_sizes=[0.1,0.2,0.4,0.6,0.8,1],cv=10,scoring='accuracy')
    train_sizes,train_score,test_score = learning_curve(BernoulliNB(),datasets,labelsets,train_sizes=[0.1,0.2,0.4,0.6,0.8,1],cv=10,scoring='accuracy')
    
    train_error = 1 - np.mean(train_score,axis=1)
    test_error = 1 - np.mean(test_score,axis=1) 
    plt.plot(train_sizes,train_error,'o-',color='r',label='training')
    plt.plot(train_sizes,test_error,'o-',color = 'g',label='testing')   
    plt.legend(loc='best')
    plt.xlabel('traing examples')
    plt.ylabel('error')
    plt.show()

if __name__ == "__main__":

    # check_test = ['这部电影很垃圾，不值得一看','电影真的没什么意思，建议大家不要去看','电影非常不错，推荐给各位','刘浩然演的非常不错，支持支持']
    # label_list = [0,0,1,1]
    new_list = []
    wordslist,scorelist =Comments_process(0)
    
    # wordslist ,scorelist = wordpro.Mongo_process(10000)
    # print(wordslist)
    # print(scorelist)

    comment_vec = CommonFeature(wordslist)
    print(comment_vec)
    # poly = PolynomialFeatures(2)
    # comment_vec = poly.fit_transform(comment_vec)
    # print(comment_vec)
    comment_train,comment_test,target_train,target_test = train_test_split(comment_vec,scorelist,test_size = 0.25,random_state = 0)  
    
    # 朴素贝叶斯三种模式：高斯、多项式、伯努利
    wyNB = MultinomialNB(alpha=100.0)
    # wyNB = GaussianNB()
    # recall_score()
    # wyNB = BernoulliNB()
    # 简单测试一下
    # for com in check_test:
    #     new_list.append(Jieba_process(str(com)))
    #     # print(com)
    # new_list = CommonFeature(new_list) 
    # test_list = train_test_split(new_list,)
    wyNB.fit(comment_train,target_train)
    # print(wyNB.predict(new_list))
    pre_list = wyNB.predict(comment_test)
    recall_score = recall_score(target_test,pre_list)
    f1_score = f1_score(target_test,pre_list,average="micro")
    acc = wyNB.score(comment_test,target_test)
    print("召回率为：")
    print(recall_score)
    print("F值为：")
    print(f1_score)
    print("准确率为：")
    print(acc)
    print("绘制Roc曲线：")
    true_target = np.array(target_test)
    print(true_target)
    pre_score = np.array(pre_list)
    print(pre_score)
    fpr,tpr,threholds = metrics.roc_curve(true_target,pre_score)
    plt.plot(fpr,tpr,marker='o')
    plt.show()
    # print("下面测试拟合程度")
    # Overfitting(comment_vec,scorelist)