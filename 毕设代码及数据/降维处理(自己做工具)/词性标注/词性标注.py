from pymongo import MongoClient
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import re
import wordcloud
import jieba.posseg as pseg
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud


"""
1.对词汇的词性进行标注，每条评论的词汇单独进行分词，然后对于每个词汇的词性，剔除个别单词
2.保留动词（V）、区别词（b）、副词（d）、状态词（z）、状态词（zg）、形容词（a）
"""



def Mongo_process(wy):
    """
    函数说明：读取mongodb数据，数据存储list
    wy:数据库读取数量
    """

    comments_list = []     
    connect = MongoClient('localhost',27017)
    db = connect.douban

    if wy == 0:
        comments = db.movie.find()
    else:
        comments = db.movie.find().limit(wy)

    for info in comments:
        # 读取数据库，并做相关处理 正则表达式、jieba分词等
        if(len(info['comment_info'])):
            # 仅处理评论不为空的评论
            # 正则表达式处理把表情、符号、数字、英文全部去除
            info['comment_info'] = ReHtml_process(str(info['comment_info']))
            # 结巴分词处理
            info['comment_info'] = Jieba_process(str(info['comment_info']))
            # 停用词处理
            info['comment_info'] = Stopwords_process(str(info['comment_info']))
            # 评论数据汇总至List中，进行下一步操作——词频统计、词云生成
            comments_list.append(info['comment_info'])
            # TFIDF(info['comment_info'],5,True)
            wordsproperty(info['comment_info']) 

def Stopwords_process(infostr):
    """
    去除停用词
    """
    stopwords = [line.strip() for line in open('哈工大停用词表.txt','r',encoding='utf-8').readlines()] 
    outstr=""
    for word in infostr:
        if word not in stopwords:
            outstr+=word
            # outstr+=""
    print(outstr)
    return outstr

def Jieba_process(infostr):
    # 出去空格，链接成一句话，无论是否通顺
    # 通过加入jieba自定义词库提高分词的准确率
    jieba.load_userdict("../../jieba词库/jieba自定义词库.txt")
    stopstr = ''.join(infostr.split())
    stopstr = jieba.cut(stopstr,cut_all=False)
    stopstr = ' '.join(stopstr)
    return stopstr

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


def wordsproperty(comment):
    words = pseg.cut(comment)
    for word ,flag in words:
        if word ==' ':
            pass
        elif :
            
    
if __name__ == "__main__":
    Mongo_process(1)