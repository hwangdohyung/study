from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D,Flatten # 이미지 작업은 2차원

model = Sequential()
# model.add(Dense(units=10, input_shape=(3,))) #(batch_size, input_dim)
# model.summary()
# (input_dim + bias) *units = summary Param 갯수(Dense 모델)

model.add(Conv2D(filters=10, kernel_size=(2,2),   #출력:(N,4,4,10)
                 input_shape = (5, 5, 1)))   #(batch_size(행의갯수)=rows, columns , channels)
model.add(Conv2D(7, (2,2),activation ='relu'))    #출력:(N,3,3,7)
model.add(Flatten()) #(N, 63) #평탄화 작업(flatten) 
model.add(Dense(32,activation = 'relu'))
model.add(Dense(32,activation = 'relu'))
model.add(Dense(10,activation = 'softmax'))

model.summary() 
# (kernel_size * channels +bias) *filters = summary Param 갯수(CNN 모델)
# 
#CNN input: none, row, column , channel 
#    output: none, row , column, filter

#DNN input: none, input_dim 
#    output: none, unit(output)

# Dense layer로 변환할때
#- 4차원 ->2차원으로 바꾸는것 데이터를 쭉 늘인다.(reshape) 순서는 바뀌지 않음. (n,4,3,2)-> (n,24) 
