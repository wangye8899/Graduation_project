from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import jieba
import csv 
import pandas as pd
import gc
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn import svm
def Comments_proccess(wy):
    scorelist = []
    wordslist = []
    """
    函数说明：读Mongo然后做初步处理,将数据库中的评论数据，生成list，并返回给CountVec使用，生成词向量
    wy：传入的数据库读取条数，0代表全部读取
    """
    connect = MongoClient('localhost',27017)
    db = connect.douban
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

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
            # 处理分数
            info['comment_score'] = Score_process(info['comment_score'])
            scorelist.append(info['comment_score'])
            wordslist.append(info['comment_info'])
    # print(wordslist)
    return wordslist,scorelist     

 
# 通过临时写文件转存数据
# 调用函数开始求解
def StopWords(wordslist):
    with open('../../stopwords/stopwords/哈工大停用词表.txt','rb') as fp:
        stopword = fp.read().decode('utf-8')
    stopwordsList = stopword.splitlines()
    # print(stopwordsList)
    count_vec = CountVectorizer(stop_words = stopwordsList)
    return count_vec,wordslist

def SumFeature(wordslist):
    """
    统计一下停用词处理前的特征数 、以及停用词处理后的特征数
    """
    vec = CountVectorizer()
    notStopWords = pd.DataFrame(vec.fit_transform(wordslist).toarray(),columns=vec.get_feature_names())
    print("未经过停用词处理的特征数为%s"%notStopWords.shape[1])

def VecProcess(count_vec,wordslist):
    # 讲所有数据集转化为词向量
    comment_vec = count_vec.fit_transform(wordslist).toarray()
    hasStopWord = pd.DataFrame(count_vec.fit_transform(wordslist).toarray(),columns=count_vec.get_feature_names())
    print("已经经过通用词处理后的特征数为%s"%hasStopWord.shape[1])
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

def CommonFeature(wordslist):
    """
    平凡特征词处理，>0.8即为平凡 ，<5即为特征
    """
    # print(wordslist)
    with open('../../stopwords/stopwords/哈工大停用词表.txt','rb') as fp:
        stopword = fp.read().decode('utf-8')
    stopwordsList = stopword.splitlines()
    vect=TfidfVectorizer(binary=False,decode_error='ignore',max_df=0.8,min_df=2,stop_words=stopwordsList)
    # vect = CountVectorizer(max_df=0.5,min_df=5,stop_words=stopwordsList)
    comment_vec = vect.fit_transform(wordslist).toarray()
    # print(comment_vec)
    print("共有数据%s"%len(comment_vec)+"条")
    # print(comment_vec)
    # 使用pandas工具统计特征数
    MaxMin = pd.DataFrame(vect.fit_transform(wordslist).toarray(),columns=vect.get_feature_names())
    print("去除停用词、平凡词和特征词后的特征总数为：%s"%MaxMin.shape[1])
    return comment_vec
    
def ReadFileTOVec(filename):
    wordslist = []
    scorelist = []
    f = open(filename,"r")
    content = f.readlines()
    for con in content:
        wordslist.append( str(con.split('$')[0]))
        scorelist.append(str(con.split('$')[1]).replace('\n',''))
    return wordslist,scorelist

if __name__ == "__main__":

    # 从数据库中拿到分词列表，得分列表
    # wordslist,scorelist = Comments_proccess(20000)
    wordslist , scorelist = ReadFileTOVec("02评论数据集分词结果.txt")

    # print(wordslist)
    # print(scorelist)
    comment_vec = CommonFeature(wordslist)
    comment_train,comment_test,target_train,target_test = train_test_split(comment_vec,scorelist,test_size = 0.25,random_state=0)
    wytrain = svm.SVC(C=10,kernel = 'linear')
    
    # c_range = np.logspace(-5, 15, 11, base=2)
    # gamma_range = np.logspace(-9, 3, 13, base=2)
    # # 网格搜索交叉验证的参数范围，cv=3,3折交叉
    # param_grid = [{'kernel': ['linear'], 'C': c_range, 'gamma': gamma_range}]
    # grid = GridSearchCV(wytrain, param_grid, cv=3, n_jobs=-1)
    # clf = grid.fit(comment_train,target_train)
    # score = grid.score(comment_test,target_test)
    # print(score)
    wytrain.fit(comment_train,target_train)
    acc = wytrain.score(comment_test,target_test)
    print(acc)
    # com_list = list(wytrain.predict(comment_test))
    # num = 0
    # for i in range(len(com_list)):
    #     if com_list[i]==target_test[i]:
    #         num+=1
    # print(num)
    # print(len(target_test))
    # print(float(num/len(target_test)))
    # print(comment_test)
    # print(com_list)
    # print(target_test)
    # print()
    

    