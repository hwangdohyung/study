import numpy as np 
from sklearn.datasets import load_digits
from tensorflow.python.keras.models import Sequential,Model,load_model
from tensorflow.python.keras.layers import Dense,Input
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,accuracy_score
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler,StandardScaler,MaxAbsScaler,RobustScaler
import datetime

#1.데이터 
datasets = load_digits()
x= datasets.data
y= datasets.target

print(x.shape, y.shape) #(1797, 64) (1797, ) * 64개의 컬럼이 아니라 8x8 이미지 (64칸) 그게 1797개가 있다.
print(np.unique(y,return_counts=True)) #y의 라벨 ,[0 1 2 3 4 5 6 7 8 9]

from tensorflow.keras.utils import to_categorical
y = to_categorical(y)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3,shuffle=True,
                                                     random_state=58)

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.fit_transform(x_train)#스케일링한것을 보여준다.
x_test = scaler.transform(x_test)#test는 transfrom만 해야됨 

#2.모델
input1=Input(shape=(64,))
dense1=Dense(40,activation='relu')(input1)
dense2=Dense(40,activation='relu')(dense1)
dense3=Dense(40,activation='relu')(dense2)
dense4=Dense(40,activation='relu')(dense3)
dense5=Dense(40,activation='relu')(dense4)
output1=Dense(10,activation='softmax')(dense5)
model=Model(inputs=input1,outputs=output1)

date= datetime.datetime.now()
date = date.strftime('%m%d_%H%M')

#3.컴파일,훈련
model.compile(loss= 'categorical_crossentropy', optimizer ='adam', metrics='accuracy') #다중분류는 무조건 loss에 categorical_crossentropy
 #분류모델에서 셔플 중요! ,false로 하면 순차적으로 나와서 2가 아예 안나옴.

earlyStopping= EarlyStopping(monitor='val_loss',patience=30,mode='min',restore_best_weights=True,verbose=1)

filepath = './_ModelCheckpoint/k24/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'

mcp = ModelCheckpoint(monitor='val_loss',node='auto',save_best_only=True,verbose=1,
                      filepath="".join([filepath,'digit',date,'_',filename]))

model.fit(x_train, y_train, epochs=1000, batch_size=32,validation_split=0.2,callbacks=[earlyStopping,mcp] ,verbose=1)
#4.평가,예측

results = model.evaluate(x_test,y_test)
print('loss : ', results[0])

y_predict = model.predict(x_test) 
y_predict = y_predict.argmax(axis=1) 

y_test = y_test.argmax(axis=1) 
acc = accuracy_score(y_test,y_predict)
print('acc : ',acc)
