
import numpy as np 
from tensorflow.python.keras.models import Sequential,load_model
from tensorflow.python.keras.layers import Dense,Dropout,LSTM,Conv1D,Flatten
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint 
import datetime

#1.데이터
datasets = load_boston()
x,y = datasets.data, datasets.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True, random_state=66)
                                                                                                                         
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)                 
x_test = scaler.transform(x_test)

print(x_train.shape)
x_train= x_train.reshape(404,13,1)
x_test = x_test.reshape(102,13,1)

#2.모델구성
model = Sequential()
model.add(Conv1D(200,2,activation='relu', input_shape=(13,1))) 
model.add(Flatten())
model.add(Dense(100,activation= 'relu'))
model.add(Dense(100,activation= 'relu'))
model.add(Dense(100,activation= 'relu'))
model.add(Dense(100,activation= 'relu'))
model.add(Dense(1))

#시간
date = datetime.datetime.now()
print(date)                       
date = date.strftime('%m%d_%H%M') 
print(date)

# 3.컴파일,훈련
model.compile(loss='mse', optimizer='adam')

earlyStopping = EarlyStopping(monitor= 'val_loss',patience=20,mode='min',restore_best_weights=True,verbose=1)

# filepath = './_ModelCheckpoint/k24/'
# filename = '{epoch:04d}-{val_loss:.4f}.hdf5'

# mcp = ModelCheckpoint(monitor='val_loss', mode='auto',verbose=1,
#                       save_best_only=True,filepath= "".join([filepath ,'boston',date,'_', filename]))

hist = model.fit(x_train,y_train,epochs=500,batch_size=128,verbose=1,validation_split= 0.2,callbacks=[earlyStopping])


#4.평가,예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)
y_predict = model.predict(x_test) 
r2 = r2_score(y_test, y_predict) 
print('r2스코어 : ' , r2) 

#dropout: 평가,예측할때는 적용안됨. 데이터를 다시 채워서 함.

#DNN
# loss :  10.864871978759766
# r2스코어 :  0.870010874320327

#LSTM
# loss :  75.4331283569336
# r2스코어 :  0.09750564038152243

#Conv1D
# loss :  12.524384498596191
# r2스코어 :  0.8501562183738237