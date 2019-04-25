"""
绘制
"""
import matplotlib.pyplot as mat
x1 = [1,2,3,4]
y1 = [1.2,3.2,2.3,4.5]
x2 = [3,4,5,6]
y2 = [7,8,9,11]
# mat.plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
# mat.plot(y,'r+')
# mat.plot([1,2,3], [1,4,9], 'cs',  label='line 2')
mat.plot(x1, y1, color='green', linestyle='dashed', marker='s',
     markerfacecolor='blue', markersize=12)
mat.show()
