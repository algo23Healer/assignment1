from factor_construct import *


factor = factor(data)
x = factor.get_all_factors()
x.drop(x.tail(2).index,inplace=True) 
x = x.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
y = factor.goal()
y.drop(y.tail(2).index,inplace=True) 
clf_linear = svm.SVC(kernel='linear', C=1.0, gamma=10)   # kernel = 'linear'

train_x = x.iloc[0:300,:]
train_y = y.iloc[0:300,0]
test_x = x.iloc[300:496,:]
test_y = y.iloc[300:496,:]
# train_y = train_y.T.iloc[0,:]
# test_y = test_y.T.iloc[0,:]
clf_linear.fit(train_x,train_y)

score_linear_train = clf_linear.score(train_x,train_y)
score_linear_test = clf_linear.score(test_x,test_y)
# y_pred = clf_linear.predict(x_test)
print('The prediction score of the train is:', score_linear_train)
print('The prediction score of the test is:', score_linear_test)