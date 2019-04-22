

import numpy as np
import mmap as mp

def loadFile(filename):
    """
    1.函数说明;加载数据集 包括训练集 测试集
    2.filename：文件路径
    3.return：文件返回词条 邮件的类别分类
    """
    # 分词列表 评论分类列表
    contentList = []
    classVec = []
    file = open(filename)
    # 读取文件中的所有行
    contents = file.readlines()
    
    for line in contents:
        content = line.strip('\n').split(' ')
        # print(line)
        classVec.append(int(content[0]))
        del(content[0])
        while '' in content:
            content.remove('')
        contentList.append(content)
    file.close()
    
    # print(contentList)
    # print(classVec)
    print("已经将分词后的影评，转换成了词汇列表和对应的词向量")
    return contentList,classVec 

def createVocabList(dataSet):
    """
    1.函数说明： 生成词汇表 并去除重复的词汇
    2.dataset： 通过loadFile函数生成的列表型评论词汇数据
    3.返回不重复的评论词汇
    """
    # 使用set的数据结构 去除重复的词汇
    vocabList = set([])
    for doc in dataSet :
        vocabList = vocabList | set(doc) 
    # 以列表的形式返回 不重复词汇的集合
    print(len(vocabList))
    return list(vocabList)


def Words_to_vec(vocabList,wordSet):
    """
    1.函数说明：根据vocabList词汇表 将每个评价分词后在进行向量化 即出现为1 不出现为0
    2.vocablit: 词汇表
    3.wordSet: 生成的词向量
    return：返回的词向量
    """
    
    returnVec = [0]*len(vocabList)

    for word in wordSet:
        if word in vocabList:
            # 如果在词汇表中的话 便将其所在位置赋为1
            returnVec[vocabList.index(word)] = 1
        else:
            pass
    
    return returnVec

def trainNB(trainMat,trainLabel):
    """
    1.函数说明：朴素贝叶斯训练函数
    2.trainMat：训练文档的词向量矩阵ss
    3.trainLable：训练数据的类别标签
    4.return:
        p0vec:消极情感的评论
        p1vec:积极情感的评论
        p_positive:积极评论的概率
        p_negative:消极评论的概率
    """
    # 训练集的数量
    numTraindocs = len(trainMat)
    # 单词数 
    numWords = len(trainMat[0])
    print("numwords%s"%numWords)
    # 积极情感类评论数量及概率
    p_positive = sum(trainLabel) /float(numTraindocs)
    p_negative = 1-p_positive

    p_positiveNum = np.ones(numWords)
    p_negativeNum = np.ones(numWords)

    p_positiveDemo = 2.0
    p_negativeDemo = 2.0

    for i in range(numTraindocs):
        if trainLabel[i] == 1:
            # 如果是积极情感的话，则统计积极情感评论的个数
            p_positiveNum += trainMat[i]
            p_positiveDemo += sum(trainMat[i])
        else:
            # 统计消极情感的评论
            p_negativeNum += trainMat[i]
            p_negativeDemo += sum(trainMat[i])

    print(p_negativeNum)
    print(p_positiveNum)

    p1vec = np.log(p_positiveNum/p_positiveDemo)
    p0vec = np.log(p_negativeNum/p_negativeDemo)

    return p1vec,p0vec,p_positive


def classifyNB(vec2Classify,p0vec,p1vec,p_positive):
    """
    1.函数说明：分类 比较p0 和 p1的大小 并返回相应的预测类别
    2.vec2Classify:返回的词汇表对应的词向量
    3.p0vec 消极的条件概率
    4.p1vec 积极的条件概率
    5.p_positive 积极情感的类别概率
    return:
        1:表示积极情感
        0:表示消极情感
    """
    p_positive1 = sum(vec2Classify*p1vec) + np.log(p_positive)
    p_negative0 = sum(vec2Classify*p0vec) + np.log(1-p_positive)

    if p_positive1 > p_negative0:
        return 1
    else:
        return 0


def main():
    trainList,trainLable = loadFile('训练集.txt')
    # trainList,trainLable = loadFile('训练集.txt')
    # print(trainList)
    vocabList =createVocabList(trainList)
    # print(vocabList)
    trainMat = []
    cnt = 0
    
    
    for train in trainList:
        trainMat.append(Words_to_vec(vocabList,train))
        cnt+=1
        # print("当前正在处理%s组训练数据"%cnt)
  
    print("训练集数据处理完毕")
    p1vec,p0vec,p_positive = trainNB(np.array(trainMat,dtype='float16'),np.array(trainLable,dtype='float16'))
    print("生成训练集指标")
    print(p1vec)
    print(p0vec)
    print(p_positive)
    # 加载测试集数据进行测试
    # testList ,testLable = loadFile('新测试.txt')
    testList ,testLable = loadFile('测试集.txt')
    resultMat = []
    nn = 0
    for test in testList:
        doc = np.array(Words_to_vec(vocabList,test))

        if classifyNB(doc,p0vec,p1vec,p_positive):
            #print("积极")
            resultMat.append(1)
        else:
            resultMat.append(0)
            #print("消极")
        nn+=1
        # print("正在处理第%s条数据"%nn)
    cc = 0
    for i  in range(len(testLable)):
        if testLable[i] == resultMat[i]:
            cc+=1
    print("准确率为："+str(100*cc/float(len(testLable)))+"%")


if  __name__ == '__main__':
    main()