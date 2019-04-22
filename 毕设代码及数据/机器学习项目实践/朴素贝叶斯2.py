'''
对电子邮件进行分类
'''
import numpy as np
import mmap as mp
def loadFile(filename):
    """
    ：函数说明： 加载数据集 包括测试集和训练集
    ：filename:文件路径
    ：return 文件的返回词条 邮件的类别向量 
    """   
    # 使用python mmap模块 实现对文件的内存映射
    # 词条列表 邮件向量列表   
    contentList=[]
    classVec = []
    # with open(filename,'r') as f:
    #     m = mp.mmap(f.fileno(),0,access=mp.ACCESS_READ)
    #     contents = m[:-1]
    file = open(filename)
    contents = file.readlines()
    for line in contents:
        # 以空格的形式切分字符串
        content = line.strip('\n').split(' ')
        print("输出的content"+str(content))
        # 取到邮件的类别标签
        classVec.append(int(content[0]))
        del(content[0])
        contentList.append(content)
    file.close()
    return contentList,classVec


def createVocabList(dataSet):
    """
    ：函数说明:生成词汇表 并去除重复的词汇
    ：dataSet: 切分所有邮件而得到的词条
    ：返回不重复单词的词汇表 
    """
    # 使用set的数据结构 去除重复的单词
    vocabList = set([])
    for doc in dataSet:
        vocabList = vocabList | set(doc)
    #以list形式返回词汇表 
    return list(vocabList)


def Words_to_Vec(vocabList,wordsSet):
    """
    函数说明：根据vocabList词汇表 将每个wordSet词条向量化 1表示出现 0 表示没有出现
    vocabList：词汇表
    wordsSet :切分每封邮件得到的词条
    return : 返回的词条向量
    """
    returnVec = [0]*len(vocabList)

    for word in wordsSet:
        if word in vocabList:
            # 如果在词汇表中出现的话 便把其在词汇表中的位置 赋值为1
            returnVec[vocabList.index(word)] = 1 

        else:
            print("这个 %s 单词不在",word)

    return returnVec


def trainNB(trainMat,trainLabel):
    """
    函数说明：
    朴素贝叶斯 分类训练函数
    trainMat：
    训练文档的词向量矩阵 
    trainLabel：
    训练数据的类别标签
    return：
    p0Vec：侮辱类的条件概率数组
    p1Vec：非侮辱类的条件概率数组
    pNotAbusive：文档属于侮辱类的概率
    """
    # 训练集的数量
    numTraindocs = len(trainMat) 
    # 每个词条向量的长度
    numWords = len(trainMat[0])
    # 文档属于非侮辱类的概率 
    pNotAbusive = sum(trainLabel) / float(numTraindocs)
     
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)

    p0Denom = 2.0
    p1Denom = 2.0
    
    for i in  range(numTraindocs):
        if trainLabel[i] == 1:
            # 统计非侮辱类中各个特征出现的次数
            p1Num +=trainMat[i] 
            p1Denom += sum(trainMat[i])
        
        else:
            # 统计侮辱类的各个特征出现的次数
            p0Num += trainMat[i]
            p1Denom += sum(trainMat[i])
        
    p1Vec = np.log(p1Num/p1Denom)
    p0Vec = np.log(p0Num/p0Denom)

    return p1Vec,p0Vec,pNotAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass0):
    """
    函数说明：分类 比较p0和p1的大小 
    ve2Classify: 待分类的词条向量
    p0Vec： 侮辱类条件概率分组
    p1Vec： 非侮辱类的条件概率数组
    pClass0：邮件属于侮辱类的概率
    return ：
    1：表示非侮辱类
    0：表示侮辱类
    """
    p1 = sum(vec2Classify*p1Vec) + np.log(1-pClass0)
    p0 = sum(vec2Classify*p0Vec) + np.log(pClass0)
    if p1>p0:
        return 1
    else:
        return 0
    

def main():
    # 处理训练数据 去除所有重复的单词
    # 生成词汇表
    trainList ,trainLable = loadFile('spam_train.txt')
    vocabList = createVocabList(trainList)
    trainMat = []
    cnt = 0
    for train in trainList :
        trainMat.append(Words_to_Vec(vocabList,train))
        cnt+=1
        print("当前处理是%s组训练数据" %cnt)
    # 使用训练集数据训练分类器
   
    p1v,p0v,pAb = trainNB(np.array(trainMat,dtype='float16'),np.array(trainLable,dtype='float16'))
    
    # 加载测试集数据
    testList,testLable = loadFile('spam_test.txt')
    resultMat = []
    nn = 0
    for test in testList:
        doc = np.array(Words_to_Vec(vocabList,test))

        if classifyNB(doc,p0v,p1v,pAb):
            resultMat.append(1)
        else:
            resultMat.append(0)
        nn+=1
        print("正在处理%s组测试数据"%nn)
    cc =0 
    for i in range(len(testLable)):
        if testLable[i] == resultMat[i]:
            cc+=1

    print("准确率为："+str(100*cc/float(len(testLable)))+"%")



if __name__ == '__main__':
    main()