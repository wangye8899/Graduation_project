import KNN
from numpy import * 

dataset ,labels = KNN.createDataSet()
testx = array([1.2,1.1])
k = 3
outputLabelX = KNN.clissfy0(testx,dataset,labels,k)
testY = array([0.1,0.3])
# outputLabelY = KNN.clissfy0(testY,dataset,labels,k)

print(testx)
print(outputLabelX)
# print(testY)
# print(outputLabelY)