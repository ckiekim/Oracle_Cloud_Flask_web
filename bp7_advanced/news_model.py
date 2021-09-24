# 20 News Group 분류
import joblib
import pandas as pd 
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

train_news = fetch_20newsgroups(subset='train', random_state=2021,
                                remove=('headers', 'footers', 'quotes'))
df_train = pd.DataFrame(train_news.data, columns=['data'])
df_train['target'] = train_news.target
df_train.drop(df_train[df_train.data == ''].index, inplace=True)

test_news = fetch_20newsgroups(subset='test', random_state=2021,
                                remove=('headers', 'footers', 'quotes'))
df_test = pd.DataFrame(test_news.data, columns=['data'])
df_test['target'] = test_news.target
df_test.drop(df_test[df_test.data == ''].index, inplace=True)
df_test.to_csv('../static/data/news/test.csv', index=False)

X_train = df_train.data.values
y_train = df_train.target.values
print(X_train.shape, y_train.shape)

# Case 1. CountVectorizer + LogisticRegression
pipeline = Pipeline([
    ('count_vect', CountVectorizer(stop_words='english', max_df=300, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=1, max_iter=300))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/news_count_lr.pkl')
print('Case 1. CountVectorizer + LogisticRegression done.')

# Case 2. TfidfVecorizer + LogisticRegression
pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(stop_words='english', max_df=700, ngram_range=(1,2))),
    ('lr_clf', LogisticRegression(C=10, max_iter=300))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/news_tfidf_lr.pkl')
print('Case 2. TfidfVecorizer + LogisticRegression done.')

# Case 3. TfidfVecorizer + SVC
pipeline = Pipeline([
    ('tfidf_vect', TfidfVectorizer(stop_words='english', max_df=300, ngram_range=(1,1))),
    ('sv_clf', SVC(C=10))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, '../static/model/news_tfidf_sv.pkl')
print('Case 2. TfidfVecorizer + SVC done.')