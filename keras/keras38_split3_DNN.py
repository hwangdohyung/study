import numpy as np 
import numpy as np
from sklearn import metrics 
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,LSTM,GRU
from tensorflow.python.keras.callbacks import EarlyStopping

#1.데이터
a = np.array(range(1,101))
size = 5
#x는 4개 y는 1개
x_predict = np.array(range(96,106))

################################### data 자르기 ###################################
def split_x(data, y1):
    aaa= [ ]
    for i in range(len(data) - size +1): 
        subset = data[i : (i + size)] 
        aaa.append(subset)   
    return np.array(aaa)

bbb = split_x(a, size)
print(bbb)
print(bbb.shape) 

x= bbb[:, :-1]
y= bbb[:, -1]
print(x,y)

print(x.shape, y.shape) 
# x = x.reshape(96,4,1)

####################################### predict ####################################
size1= 4
def predict_x(data, y1):
    ccc= [ ]
    for i in range(len(data) - size1 +1): 
        subset = data[i : (i + size1)] 
        ccc.append(subset)   
    return np.array(ccc)

ddd = predict_x(x_predict, size1)


x_pred= ddd[:, :]

print(x_predict)
print(x_predict.shape)

#2.모델 구성
model = Sequential()
model.add(Dense(200,activation='relu',input_dim = 4))
model.add(Dense(100,activation='relu'))
model.add(Dense(100,activation='relu'))
model.add(Dense(100,activation='relu'))
model.add(Dense(1,activation='relu'))

#3.컴파일,훈련
model.compile(loss='mse', optimizer='adam')
earlyStopping = EarlyStopping(monitor= 'loss',patience=20, mode='min',restore_best_weights=True,verbose=1)
model.fit(x,y, epochs=500, batch_size=32,verbose=1,callbacks=earlyStopping)

#4.평가,예측 
loss = model.evaluate(x,y)
# y_pred=x_pred.reshape(7,4,1)
result = model.predict(x_pred)  #모델은 3차원을 원한다. 
print('loss : ', loss)
print('result : ', result)

# loss :  3.7721172702731565e-05
# result :  [[100.003784]
#  [101.00416 ]
#  [102.004555]
#  [103.00493 ]
#  [104.005325]
#  [105.00569 ]
#  [106.006096]]

