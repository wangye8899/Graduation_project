import numpy as np
from sklearn.svm import SVC

def loadFile(filename):
    """
    1.函数说明;加载数据集 包括训练集 测试集
    2.filename：文件路径
    3.return：文件返回词条 邮件的类别分类
    """
    contentList = []
    classVec = []
    file = open(filename)
    contents = file.readlines()
    print(contents)
    for line in contents:
        content = line.strip('\n').split(' ')
        classVec.append(int(content[0]))
        del(content[0])
        while '' in content:
            content.remove('')
        contentList.append(content)
    file.close()
    print("已经将分词后的影评，存入词汇列表和对应")
    return contentList,classVec


def createVocabList(dataSet):
    """
    1.函数说明： 生成词汇表 并去除重复的词汇
    2.dataset： 通过loadFile函数生成的列表型评论词汇数据
    3.返回不重复的评论词汇
    """
    vocabList = set([])
    for doc in dataSet :
        vocabList = vocabList | set(doc)
    return list(vocabList)

def Words_to_Vec(vocabList,wordSet):
    """
    1.函数说明：根据vocabList词汇表 将每个评价分词后在进行向量化 即出现为1 不出现为0
    2.vocablit: 词汇表
    3.wordSet: 生成的词向量
    return：返回的词向量
    """
    returnVec = [0]*len(vocabList)
    for word in wordSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            pass
    return returnVec


def Svm_Train(contentlist,classvec,testclassVec,testMat):
    
    clf = SVC(C=200,kernel='rbf')
    clf.fit(contentlist,classvec)
    predict_result = clf.predict(testMat)
    print(predict_result)
    cnn=0
    for i in range(len(predict_result)):
        if predict_result[i] == testclassVec[i]:
            cnn+=1
    print(float(cnn/len(predict_result)))



if __name__=='__main__':
    trainMat = []
    testMat = []
    filepath  = '测试集.txt'
    filename = '训练集.txt'
    contentList,classVec = loadFile(filename)
    testconList,testclassVec = loadFile(filepath)
    vocabList = createVocabList(contentList)
    testVocabList = createVocabList(testconList)
    allvocablist = vocabList+testVocabList
    for con in contentList:
        trainMat.append(Words_to_Vec(allvocablist,con))
    cn=0
    for tcon in testconList:
        testMat.append(Words_to_Vec(allvocablist,tcon))
        cn+=1
    print(testMat)
    Svm_Train(trainMat,classVec, testclassVec,testMat)
