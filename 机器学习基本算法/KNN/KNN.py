from numpy import * 
import operator

def createDataSet():

    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group , labels

def clissfy0(inX,dataset,labels,k):
    dataSetSize = dataset.shape[0] 
    # print(dataSetSize)
    # print(dataset.shape[1])
    # 读取矩阵的行数
    diffMat = tile(inX,(dataSetSize,1))-dataset
    # 测试点 与 待测试点逐一作差
    # 按要求生成数组
    # print(diffMat)
    sqDiffMat = diffMat ** 2
    # 作差之后求平方
    # print(sqDiffMat)
    sqDistances = sqDiffMat.sum(axis=1)
    # 求平方和
    # print(sqDistances)
    distances = sqDistances ** 0.5
    # 开根号求距离
    print(distances)
    sortedDistIndicies = distances.argsort()
    # 对距离排序返回索引
    print(sortedDistIndicies)
    classCount = {}
    for i in range(k):
        voteLabel = labels[sortedDistIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
    sortedClassCount = sorted(classCount.items(),
        key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]