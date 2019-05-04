import re
from pymongo import MongoClient
import TFIDF as tf




def loadfile(filename):
    commentlist = []
    fr = open(filename,'r')
    for line in fr.readlines():
        commentlist.append(str(line.split('$')[1]).replace('\n',''))
    # 通过一层for循环，现将所有的分词评论放到一个list中暂存
    # 接下来读取commentlist，并将每一个词语放到wordslist中，用于词频的统计
    clist = []
    wordslist = []
    for comment in commentlist:
        clist = comment.split(' ')
        for c in clist:
            wordslist.append(str(c))
        wordslist.append('$')
    # 拿到所有词语构成的wordslist
    print(len(wordslist))
    return wordslist


def Frequence_process(wordslist):
    # 对平凡词、独特词进行处理
    newwordslist = []
    for word in wordslist:
        if word != "$":
            # $用作分割，不能进行判断
            frequence = wordslist.count(word)
            snum = len(wordslist)
            if float(frequence/snum)>0.8:
                # pass
                print(str(word)+"被淘汰")
            else:
                newwordslist.append(word)
        else:
            newwordslist.append(word)
    print(len(newwordslist))
    # 3处理
    newwordslist2 = []
    for newword in newwordslist:
        if newword !="$":
            if newwordslist.count(newword)<6:
                # pass
                # 太独特
                print(str(newword)+"被淘汰")
            else:
                newwordslist2.append(newword)
        else:
            newwordslist2.append(newword)
    print(len(newwordslist2))
    print(newwordslist2)

    wordstr = " ".join(i for i in newwordslist2)    
    sublist = wordstr.split('$')
    for sub in sublist:
        if sub == ' ':
            pass
        else:
            sublist.remove(sub)
    print(sublist)

# if __name__ == "__main__":
#     name = '平凡独特词处理后的数据集.txt'
#     tf.Comments_proccess(1000,name)
#     wordlist = loadfile(name)
#     Frequence_process(wordlist)