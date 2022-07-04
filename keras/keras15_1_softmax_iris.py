#다중분류 point) --- loss categorical!, softmax ,마지막 노드갯수!,one hot encoding
import numpy as np 
from sklearn.datasets import load_iris
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,accuracy_score
from tensorflow.python.keras.callbacks import EarlyStopping

import tensorflow as tf
tf.random.set_seed(66) # tensorflow의 y=wx weight 랜덤난수 고정하는것 장단점이 있다.

#1.데이터
datasets = load_iris()
# print(datasets.DESCR)
# print(datasets.feature_names)

x= datasets['data']
y= datasets['target']
# print(x)
print(y)
# print(x.shape,y.shape) #(150,4) (150, )


#분류모델은 모델 전에 one hot encoding 필수(전처리과정)
#################### one hot encoding ####################### 2가지 방법
print('y의 라벨값 : ', np.unique(y,return_counts=True)) #무슨값으로 이루어져 있는지 확인하는것(0,1,2) #return:각각 몇개인지 확인

#텐서플로우
from tensorflow.keras.utils import to_categorical
y = to_categorical(y)
print(y)
print(y.shape)
###################

#사이킷런#
# from sklearn.preprocessing import OneHotEncoder
# one=OneHotEncoder


#2.모델
model = Sequential()
model.add(Dense(10, input_dim=4))
model.add(Dense(10,activation ='relu'))
model.add(Dense(10,activation ='relu'))
model.add(Dense(10,activation ='relu'))
model.add(Dense(10,activation ='relu'))
model.add(Dense(3,activation ='softmax')) #소프트맥스는 모든 연산값의 합이 1.0,그중 가장 큰값(퍼센트)을 선택,so 마지막 노드3개* y의 라벨의 갯수
#softmax는 아웃풋만 가능 히든에서 x

#3.컴파일,훈련
model.compile(loss= 'categorical_crossentropy', optimizer ='adam', metrics='accuracy') #다중분류는 무조건 loss에 categorical_crossentropy
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3,shuffle=True,
                                                     random_state=58) #분류모델에서 셔플 중요! ,false로 하면 순차적으로 나와서 2가 아예 안나옴.

earlyStopping= EarlyStopping(monitor='val_loss',patience=30,mode='min',restore_best_weights=True,verbose=1)

model.fit(x_train, y_train, epochs=1000, batch_size=1,validation_split=0.2,callbacks=earlyStopping, verbose=1)

#4.평가,예측
# loss,acc = model.evaluate(x_test,y_test)
# print('loss : ', loss)
# print('accuracy : ', acc)
#################### 위와 동일###############
results = model.evaluate(x_test,y_test)
print('loss : ', results[0])
print('accuracy : ', results[1])
############################################

# print(y_test)
y_predict = model.predict(x_test) # x값 4번째까지
y_predict = y_predict.argmax(axis=1) # 최대값의 위치 구해줌. argmin은 최솟값 (n, 3)에서(n, 1)로 변경됨.


y_test = y_test.argmax(axis=1) # y_test 값도 최대값 추출해줘야함 (n, 3) 에서 (n, 1)로 변경 
acc = accuracy_score(y_test,y_predict)# acc 정수값을 원한다. 
print('acc : ',acc)

print(y_predict)
print(y_test)




# #에러와 버그의 차이 : 에러는 멈춘다. 문제점 찾을 수 있다. 버그는 작동이됨.

# loss :  0.05558538809418678
# accuracy :  0.9666666388511658

# loss :  0.018528694286942482
# accuracy :  1.0