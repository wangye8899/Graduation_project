import logging
import time
import codecs
import sys
import jieba
from gensim.models import word2vec
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re




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

# def pkuseg_process(infostr):
    # 去除空格，连接成一句话。
    # stopstr = ''.join(infostr.split())
    # seg = pkuseg.pkuseg()
    # text = seg.cut(stopstr)
    # print(text)
    # # stopstr = ' '.join(stopstr)
    # # print(stopstr)
    # return stopstr

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


def More_process(wordslist):
    word_collection = []
    for com in wordslist:
        word_collection.append(str(com).split(" "))
    return word_collection 


def train_word2Vec(word_collection):
    # 设置初始时间
    t1 = time.time()
    # 控制台输出日志
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)
    # 生成word2vec模型
    model = word2vec.Word2Vec(word_collection,size=100, window=5, min_count=1, workers=6)
    # model.wv.save_word2vec_format(config.vector_word_filename, binary=False)
    model.wv.save_word2vec_format('词向量模型',binary=False)
    # 计算训练词向量共计花费时间
    print('-------------------------------------------')
    print("Training word2vec model cost %.3f seconds...\n" % (time.time() - t1))


if __name__ == "__main__":
    words,scores = Comments_process(20)
    wordvec = More_process(words)
    # print(word2vec)
    train_word2Vec(wordvec)