import pandas
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

pa = pandas.read_csv('影评训练.csv')
x=pa[['comment']]
y=pa[['star']]
max_df = 0.8
min_df = 4

vect  = CountVectorizer(max_df = max_df,min_df = min_df,token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b')

X_train,X_test,y_train,y_test = train_test_split(x,y,random_state=1)
term_matrix = pandas.DataFrame(vect.fit_transform(X_train.comment).toarray(), columns=vect.get_feature_names())
print(term_matrix)