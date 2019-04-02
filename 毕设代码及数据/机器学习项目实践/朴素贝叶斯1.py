'''
使用朴素贝叶斯，对侮辱性文本和非侮辱性文本进行分类
'''
from __future__ import print_function
from numpy import *
"""
p(xy)=p(x|y)p(y)=p(y|x)p(x)
p(x|y)=p(y|x)p(x)/p(y)
"""

# 项目名：自动屏蔽社区留言板中的侮辱性内容

def loadDataSet():
    # 创建数据集
    # 自定义的数据集和向量 
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'], #[0,0,1,1,1......]
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 代表侮辱性词汇 , ０　不是
    return  postingList,classVec




# 利用set集合数据结构 构造两个集合的并集 最终返回不重复单词的列表
def createVocabList(dataset):
    # 此函数用于返回所有 不重复单词的列表
    vocabSet = set([])
    # 声明一个空集合
    for document in dataset:
        # 求两个集合的并集 也就是去除重复的单词
        vocabSet = vocabSet|set(document)
    return list(vocabSet)


def setofWords2Vec(vocablist,inputSet):
    # 32 6
    # 创建一个和不重复词汇表等长的向量  并将元素均设为0
    returnVec = [0]*len(vocablist)
    # 遍历文档中的所有单词，如果出现词汇表中的单词，则把向量对应值设为1
    for word in inputSet:
        if word in vocablist:
            returnVec[vocablist.index(word)] = 1 
        else:
            print("the word   :%s is not in my vocabulary " %word)

    return returnVec
    # 返回的是每一个输入数据集 对应词汇表中出现的位置
    



# 初级版本
def _trainNB0(trainMatrix,trainCategory):

    print(trainMatrix)
    # 得到文件数
    numTrainDocs = len(trainMatrix)
    # print(numTrainDocs)
    # 得到单词数
    numWords  =  len(trainMatrix[0])
    # print(numWords)
    # 计算侮辱性文件出现的概率 其中1代表侮辱性 0 代表相反 则当前文件的元素值和即为侮辱性文件的个数 p(ci)
    # print(sum(trainCategory))
    # pAbusive 实际就是文档中侮辱性文档的概率
    pAbusive = sum(trainCategory)/float(numTrainDocs)


    # 构造单词出现次数列表
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)

    # 整个数据集单词出现的次数
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        # 遍历文件如果是侮辱性文件 就计算侮辱性文件中的侮辱性单词的个数
        if trainCategory[i] == 1 :
            print(trainMatrix[i])
            p1Num += trainMatrix[i] 
            p1Denom += sum(trainMatrix[i])
           
        else:
            # 如果不是侮辱性文件 则计算非侮辱性文件中侮辱性单词出现的个数
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # 类别1，即侮辱性文档的[P(F1|C1),P(F2|C1),P(F3|C1),P(F4|C1),P(F5|C1)....]列表
    # 即 在1类别下，每个单词出现次数的占比
    p1Vect = p1Num/p1Denom
    # 类别0，即正常文档的[P(F1|C0),P(F2|C0),P(F3|C0),P(F4|C0),P(F5|C0)....]列表
    # 即 在0类别下，每个单词出现次数的占比 
    p0Vect = p0Num / p0Denom
    return p0Vect,p1Vect,pAbusive


def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    """
    使用算法：
        # 将乘法转换为加法
        乘法：P(C|F1F2...Fn) = P(F1F2...Fn|C)P(C)/P(F1F2...Fn)
        加法：P(F1|C)*P(F2|C)....P(Fn|C)P(C) -> log(P(F1|C))+log(P(F2|C))+....+log(P(Fn|C))+log(P(C))
    :param vec2Classify: 待测数据[0,1,1,1,1...]，即要分类的向量
    :param p0Vec: 类别0，即正常文档的[log(P(F1|C0)),log(P(F2|C0)),log(P(F3|C0)),log(P(F4|C0)),log(P(F5|C0))....]列表
    :param p1Vec: 类别1，即侮辱性文档的[log(P(F1|C1)),log(P(F2|C1)),log(P(F3|C1)),log(P(F4|C1)),log(P(F5|C1))....]列表
    :param pClass1: 类别1，侮辱性文件的出现概率
    :return: 类别1 or 0
    """
    # 计算公式  log(P(F1|C))+log(P(F2|C))+....+log(P(Fn|C))+log(P(C))
    # 使用 NumPy 数组来计算两个向量相乘的结果，这里的相乘是指对应元素相乘，即先将两个向量中的第一个元素相乘，然后将第2个元素相乘，以此类推。
    # 我的理解是：这里的 vec2Classify * p1Vec 的意思就是将每个词与其对应的概率相关联起来
    # 可以理解为 1.单词在词汇表中的条件下，文件是good 类别的概率 也可以理解为 2.在整个空间下，文件既在词汇表中又是good类别的概率

    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)

    if p1 > p0:
        return 1 
    else:
        return 0 

def testingNB():
    # 加载数据集
    listoPosts , listClasses = loadDataSet()
    # 创建单词集合
    myVocabList = createVocabList(listoPosts)
   
    # print(len(myVocabList))
    # 计算单词是否出现并创建数据矩阵
    trainMat = []
   
    for postinDoc in listoPosts:
        trainMat.append(setofWords2Vec(myVocabList,postinDoc))
        # 训练数据
       
    pov,p1v,pab = _trainNB0(array(trainMat),array(listClasses))
    # 测试数据
    testEntry = ['love','my','dalmation']
    thisDoc = array(setofWords2Vec(myVocabList,testEntry))
    print("classDoc")
    print(thisDoc)
    print(testEntry,"分类为",classifyNB(thisDoc,pov,p1v,pab))    

testingNB()


    


        


