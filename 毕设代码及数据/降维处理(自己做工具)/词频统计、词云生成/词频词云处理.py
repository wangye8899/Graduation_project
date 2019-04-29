
from pymongo import MongoClient
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import re
import wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud

"""
1、实现TFIDF、TextRank的特征值计算
2、并根据特征值生成词云
3、统计词频
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
    comments = ''.join(comments_list) 
    return comments

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


# Mongo_process(2)
# 以下两个方法为尝试使用jieba对文本提取和关键字的算法，不过感觉TFIDF处理不是很科学,先当做一个疑问点吧，有时间查看jieba源码研究一下

def TFIDF(sentence,topK,weight):
    # 在不指定词性的条件下 提取TFIDF特征值
    # 有个疑问，JIEBA的TFIDF算的是单句话还是整个文档？
    """
    函数说明：处理每一句评论的词语TFIDF值，并取前topK个
    sentence；待提取的文本
    topK:提取的关键词数量
    weight：TFIDF权重
    """
    tags = jieba.analyse.extract_tags(sentence,topK=topK,withWeight=weight)
    
    worddic = dict()
    for info in tags:
        worddic[info[0]] = info[1]
    return worddic
    # print(tags)
def TextRank(sentence,topK,weight):
    """
    函数说明：处理每一句评论的词语TextRank值，并取前topK个
    sentence；待提取的文本
    topK:提取的关键词数量
    weight：TFIDF权重
    """
    tags = jieba.analyse.textrank(sentence,topK=topK,withWeight=weight)
    worddic = dict()
    for info in tags:
        worddic[info[0]] = info[1]
    return worddic
    # print(tags)

def Frequence(wordslist):
    """
    函数说明：统计词频,用作工具，此后可以根据词频手动添加停用词
    """

    allwords_list = []
    # 汇总左右词汇，去除''
    for info in wordslist:
        for word in info.split(' '):
            if word=='':
                pass
            else:
                allwords_list.append(word)
    fredict = {}
    # 统计词频,并按照词频大小降序排列
    # f = open('词频文件.txt','a')
    for one in allwords_list:
        num = allwords_list.count(str(one))
        fredict[one] = num 
        # f.write(str(one)+"  "+str(num)) 
        # f.write('\n')
    fredict = sorted(fredict.items(),key = lambda x:x[1],reverse = True)
    print(fredict)       


def Draw_wordcloud(dict):
    # 根据TFIDF特征值、TextRank特征值生成的词云
    back_pic = plt.imread('下载.png') 
    wc = WordCloud(font_path='font.TTF',
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_pic,  # 设置背景图片
    )
    wc.generate_from_frequencies(dict)
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file("1.jpg")
   

if __name__ == "__main__":
    
    comments = Mongo_process(20)
    Tfdic = TFIDF(comments,50,True)
    Draw_wordcloud(Tfdic)
    Textdic = TextRank(comments,100,True)
