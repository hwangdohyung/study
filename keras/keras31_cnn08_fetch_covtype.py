import numpy as np 
from sklearn.datasets import fetch_covtype
from tensorflow.python.keras.models import Sequential,Model,load_model
from tensorflow.python.keras.layers import Dense,Input,Dropout,Flatten,Conv2D
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,accuracy_score
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler,StandardScaler,MaxAbsScaler,RobustScaler
import datetime
import pandas as pd

#1.데이터 
datasets = fetch_covtype()
x= datasets.data
y= datasets.target

print(x.shape, y.shape) #(581012, 54) (581012, )
print(np.unique(y,return_counts=True)) #(array[1 2 3 4 5 6 7],array[211840, 283301,  35754,   2747,   9493,  17367,  20510] )

#사이킷런
from sklearn.preprocessing import OneHotEncoder
one = OneHotEncoder(categories='auto',sparse= False)#False로 할 경우 넘파이 배열로 반환된다.
y = y.reshape(-1,1)
one.fit(y)
y = one.transform(y)



x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3,shuffle=True,
                                                     random_state=58)

print(x_train.shape,x_test.shape)


# minmax , standard
scaler = RobustScaler()
x_train = scaler.fit_transform(x_train)#스케일링한것을 보여준다.
x_test = scaler.transform(x_test)#test는 transfrom만 해야됨 

x_train = x_train.reshape(406708,9,3,2)
x_test = x_test.reshape(174304,9,3,2)
print(x_train.shape,x_test.shape)


#2.모델구성
model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(2,2), padding='same', input_shape=(9,3,2))) 
model.add(Conv2D(7, (2,2), padding='same', activation='relu'))
model.add(Conv2D(7, (2,2), padding='same', activation='relu'))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(7,activation='softmax')) 


#3.컴파일,훈련
model.compile(loss= 'categorical_crossentropy', optimizer ='adam', metrics='accuracy') #다중분류는 무조건 loss에 categorical_crossentropy
 #분류모델에서 셔플 중요! ,false로 하면 순차적으로 나와서 2가 아예 안나옴.

earlyStopping= EarlyStopping(monitor='val_loss',patience=10,mode='min',restore_best_weights=True,verbose=1)

# filepath = './_ModelCheckpoint/k24/'
# filename = '{epoch:04d}-{val_loss:.4f}.hdf5'

# mcp = ModelCheckpoint(monitor='val_loss',mode='auto',save_best_only=True,verbose=1,
#                       filepath="".join([filepath,'fetch_covtype',date,'_',filename]))

model.fit(x_train, y_train, epochs=50, batch_size=500,validation_split=0.2,callbacks=[earlyStopping,],verbose=1) #batch default :32


#4.평가,예측

results = model.evaluate(x_test,y_test)
print('loss : ', results[0])

y_predict = model.predict(x_test)
y_predict = tf.argmax(y_predict,axis=1) 

y_test = tf.argmax(y_test,axis=1) 
acc = accuracy_score(y_test,y_predict)
print('acc : ',acc)

# loss :  0.4642634391784668
# acc :  0.8038541857903433
