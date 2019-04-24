import xlrd
import xlwt
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

def read_excel():
    data=xlrd.open_workbook(r'C:\Users\bqq\Desktop\数据\评论数据集UTF-8.xlsx')
    st=data.sheets()[0]
    rows = st.nrows

    file = xlwt.Workbook()
    table_w = file.add_sheet('fc', cell_overwrite_ok=True)

    with open(r'C:\Users\bqq\Desktop\数据\评论分词结果.txt', 'w',encoding='utf-8') as f2:
        f2.write("评论分词结果：\n")

    for i in range(rows):
        seg_list = jieba.cut(str(st.cell_value(i, 1)))
        value = "  ".join(seg_list)
        value=value.encode('utf-8')
        with open(r'C:\Users\bqq\Desktop\数据\评论分词结果.txt', 'a',encoding='utf-8') as f3:
            f3.write(str(value))

read_excel()
with open(r'C:\\Users\bqq\Desktop\数据\评论分词结果.txt',encoding='utf-8') as f3:
    res1 = f3.readlines()
#从文件导入停用词表
stpwrdpath = r"C:\\Users\bqq\Desktop\数据\stop_words\哈工大停用词表.txt"
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read()
#将停用词表转换为list
stpwrdlst = stpwrd_content.splitlines()
stpwrd_dic.close()
vector = TfidfVectorizer(stop_words=stpwrdlst)
tfidf = vector.fit_transform(res1)
tfidf_model = TfidfVectorizer().fit(res1)
print(tfidf_model.vocabulary_)
