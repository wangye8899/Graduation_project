# import re 

# # python中使用正则表达式 要先编译 提高速度 

# partten = re.compile(r'hello.*\!')
# match = partten.match('hello ,ashdshaldh!')
# if match:
#     print(match.group())

# else:
#     print("没成功")


# import re

# partten = re.compile(r'\d+')

# print(partten.findall('dsadnsall1dsaalkhdla3jalsjdal4jdsa;jd4'))
# print(partten.split('dasda1dhaskjdh2dsalda4'))

# jieba关键词抽取
# import  jieba.analyse as analyse

# lines = open('NBA.txt','rb').read()
# print(lines)
# e = analyse.extract_tags(lines,topK=20,withWeight=True)
# print(" ".join(str(e) for i in e ))