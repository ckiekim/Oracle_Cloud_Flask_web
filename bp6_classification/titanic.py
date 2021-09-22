# 타이타닉 모델 만들기
import pandas as pd 
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

df_train = pd.read_csv('../static/data/titanic_train.csv')
X_train = df_train.iloc[:, 1:].values
y_train = df_train.iloc[:, 0].values
print(X_train.shape, y_train.shape)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)

joblib.dump(scaler, '../static/model/titanic_scaler.pkl')

# 1. 로지스틱 회귀
lr_clf = LogisticRegression()
params = {
    #'C': [0.1, 1, 5, 10]
    #'C': [0.05, 0.08, 0.1, 0.2, 0.5]
    'C': [0.01, 0.03, 0.05, 0.07]
}
grid_cv = GridSearchCV(lr_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('1. 로지스틱 회귀')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_lr = grid_cv.best_estimator_
joblib.dump(best_lr, '../static/model/titanic_lr.pkl')

# 2. SVM
sv_clf = SVC()
params = {
    #'C': [0.1, 1, 5, 7, 10]
    #'C': [8, 10, 12, 15, 20]
    'C': [13, 14, 15, 16, 17, 18]
}
grid_cv = GridSearchCV(sv_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('2. SVM')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_sv = grid_cv.best_estimator_
joblib.dump(best_lr, '../static/model/titanic_sv.pkl')

# 3. Random Forest
rf_clf = RandomForestClassifier()
params = {
    #'max_depth': [4, 6, 8, 10],
    'max_depth': [7, 8, 9],
    'min_samples_split': [2, 3, 4]
    #'min_samples_split': [3, 4, 5, 6]
}
grid_cv = GridSearchCV(rf_clf, param_grid=params, scoring='accuracy', cv=5)
grid_cv.fit(X_train_scaled, y_train)
print('3. Random Forest')
print(f'최고 평균 정확도: {grid_cv.best_score_:.4f}')
print('최적 파라미터:', grid_cv.best_params_)
best_rf = grid_cv.best_estimator_
joblib.dump(best_rf, '../static/model/titanic_rf.pkl')

# Test
index = int(input('Enter number> '))
df_test = pd.read_csv('../static/data/titanic_test.csv')
test_data = (df_test.iloc[index, 1:].values).reshape(1,-1)
label = df_test.iloc[index, 0]

new_scaler = joblib.load('../static/model/titanic_scaler.pkl')
test_scaled = new_scaler.transform(test_data)

pred_lr = best_lr.predict(test_scaled)
pred_sv = best_sv.predict(test_scaled)
pred_rf = best_rf.predict(test_scaled)
print(label, pred_lr[0], pred_sv[0], pred_rf[0])
