import numpy as np 
import os 
from PIL import Image 
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import keras
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from keras import layers
from keras import models

'''Path defination'''
dirdata = 'dataset/'
dirmodel = 'model/'

'''Param'''
x_data = []
y_data = []

'''function'''
def read_data():
       count = 0
       datacount = 0 # We'll use this to tally how many images are in our dataset
       label_count = 0    
       for i in os.listdir(dirdata):
              if not i.startswith('.'): # Again avoid hidden folders
                     count =  0 # To tally images of a given gesture
                     for j in os.listdir(dirdata+str(i)):
                            img = Image.open(dirdata + str(i) + '/' + j).convert('L')
                            img = img.resize((320, 120))
                            x_data.append(np.array(img))
                            y_data.append(str(i))
                            count = count + 1
                            
                     datacount = datacount + count
                     label_count += 1
                     print('Class '+str(i)+' readed')
       return label_count,datacount,x_data,y_data

def plot(train):
       accuracy = train.history['accuracy']
       val_accuracy = train.history['val_accuracy']
       loss = train.history['loss']
       val_loss = train.history['val_loss']
       epochs = range(len(accuracy))
       plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
       plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
       plt.title('Training and validation accuracy')
       plt.legend()
       plt.figure()
       plt.plot(epochs, loss, 'bo', label='Training loss')
       plt.plot(epochs, val_loss, 'b', label='Validation loss')
       plt.title('Training and validation loss')
       plt.legend()
       plt.show()
       
'''Main'''
if __name__ == "__main__":
       print('Ready to read data...\n')
       print('Reading data......\n')
       labelcount,datacount,x_data,y_data = read_data()
       print('Img data imported: '+str(datacount)+"\n")
       print('Processing...')
       le = LabelEncoder()
       y_data = le.fit_transform(y_data)
       y_data = to_categorical(y_data)
       x_data = np.array(x_data, dtype = 'float32')
       x_data /= 255  #convert all (0 - 255) pixel to (0 - 1)
       output = int(labelcount)     
       x_data = x_data.reshape((datacount, 120, 320, 1))
       print('...')
       x_train,x_further,y_train,y_further = train_test_split(x_data,y_data,test_size = 0.2)
       x_validate,x_test,y_validate,y_test = train_test_split(x_further,y_further,test_size = 0.5)       
       model=models.Sequential()
       model.add(layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(120, 320,1))) 
       model.add(layers.MaxPooling2D((2, 2)))
       model.add(layers.Conv2D(64, (3, 3), activation='relu')) 
       model.add(layers.MaxPooling2D((2, 2)))
       model.add(layers.Conv2D(64, (3, 3), activation='relu'))
       model.add(layers.MaxPooling2D((2, 2)))
       model.add(layers.Flatten())
       model.add(layers.Dense(128, activation='relu'))
       model.add(layers.Dense(output, activation='softmax'))#makesure output is len y
       model.compile(optimizer='rmsprop',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
       print('...Complete\nTraning data, please wait......\n')
       train = model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=1, validation_data=(x_validate, y_validate))
       [loss, acc] = model.evaluate(x_test,y_test,verbose=1)
       print("Traning Complete, Accuracy:" + str(acc)+'\nSaving Model...\n')
       model_json = model.to_json()
       with open(dirmodel+ "model.json", "w") as json_file:
              json_file.write(model_json)
       model.save_weights(dirmodel+"model.h5")
       print("Saved model to disk")
       plot(train)



