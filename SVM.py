# -*- coding: utf-8 -*-
"""SVMs_Part_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nygBCSqs9abYjFZhTql5MosKtmAu3GQW

## IMPORTING LIBRARIES AND LOADING DATA
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import time
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
# %matplotlib inline

# Load the CIFAR10 dataset
from keras.datasets import cifar10
baseDir = os.path.dirname(os.path.abspath('__file__')) + '/'
classesName = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
(xTrain, yTrain), (xTest, yTest) = cifar10.load_data()
xVal = xTrain[49000:, :].astype(np.float)
yVal = np.squeeze(yTrain[49000:, :])
xTrain = xTrain[:49000, :].astype(np.float)
yTrain = np.squeeze(yTrain[:49000, :])
yTest = np.squeeze(yTest)
xTest = xTest.astype(np.float)

# Show dimension for each variable
print ('Train image shape:    {0}'.format(xTrain.shape))
print ('Train label shape:    {0}'.format(yTrain.shape))
print ('Validate image shape: {0}'.format(xVal.shape))
print ('Validate label shape: {0}'.format(yVal.shape))
print ('Test image shape:     {0}'.format(xTest.shape))
print ('Test label shape:     {0}'.format(yTest.shape))

# Show some CIFAR10 images
plt.subplot(221)
plt.imshow(xTrain[0])
plt.axis('off')
plt.title(classesName[yTrain[0]])
plt.subplot(222)
plt.imshow(xTrain[1])
plt.axis('off')
plt.title(classesName[yTrain[1]])
plt.subplot(223)
plt.imshow(xVal[0])
plt.axis('off')
plt.title(classesName[yVal[1]])
plt.subplot(224)
plt.imshow(xTest[0])
plt.axis('off')
plt.title(classesName[yTest[0]])
plt.savefig(baseDir+'svm0.png')
# plt.clf()
plt.show()
# print(xTrain[0])

"""## Reshaping Data into a Vector and Normalizing it (-1 to 1)"""

print(xTrain.shape)
print(yTrain.shape)
xTrain = np.reshape(xTrain, (xTrain.shape[0], -1)) # The -1 means that the corresponding dimension is calculated from the other given dimensions.
xVal = np.reshape(xVal, (xVal.shape[0], -1))
xTest = np.reshape(xTest, (xTest.shape[0], -1))
print(xTrain.shape) 
print(xTrain[0])

#Normalize 
xTrain=((xTrain/255)*2)-1 
print(xTrain.shape)
print(xTrain[0])

#Choosing a smaller dataset
xTrain=xTrain[:3000,:]
yTrain=yTrain[:3000]
print(yTrain)
print(xTrain.shape)
print(yTrain.shape)

"""## SVM Linear Kernel"""

from sklearn import svm
svc = svm.SVC(kernel = 'linear')
svc.fit(xTrain, yTrain)
def svm_linear(c):
    svc = svm.SVC(probability = False, kernel = 'linear', C = c)
    
    svc.fit(xTrain, yTrain) 
    
    # Find the prediction and accuracy on the training set.
    Yhat_svc_linear_train = svc.predict(xTrain)
    acc_train = np.mean(Yhat_svc_linear_train == yTrain)
    acc_train_svm_linear.append(acc_train)
    print('Train Accuracy = {0:f}'.format(acc_train))
    
    # Find the prediction and accuracy on the test set.
    Yhat_svc_linear_test = svc.predict(xVal)
    acc_test = np.mean(Yhat_svc_linear_test == yVal)
    acc_test_svm_linear.append(acc_test)
    print('Test Accuracy = {0:f}'.format(acc_test)) 
    w=svc.get_params()
    print(w)
    return w

c_svm_linear = [0.0001,0.001,0.01,0.1,1,10,100]
acc_train_svm_linear = []
acc_test_svm_linear = []

for c in c_svm_linear:
    svm_linear(c)

plt.plot(c_svm_linear, acc_train_svm_linear,'.-',color='red')
plt.plot(c_svm_linear, acc_test_svm_linear,'.-',color='orange')
plt.xlabel('c')
plt.ylabel('Accuracy')
plt.title("Plot of accuracy vs c for training and test data")
plt.grid()

import os
import zipfile

local_zip = '/content/Test_images3.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/Test_images3')
zip_ref.close()

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array,load_img,array_to_img
import matplotlib.pyplot as plt
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
import h5py
import os
#f = h5py.File('/content/model.h5', 'r')
'''
with h5py.File('/content/model.h5', 'r') as f:
    print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]

    # Get the data
    data = list(f[a_group_key])
print(data)'''
# All images will be rescaled by 1./255
test_datagen = ImageDataGenerator(rescale=1./255,rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True)

# Flow training images in batches of 1 using test_datagen generator
test_generator = test_datagen.flow_from_directory(
        '/content/Test_images3/Test_images3/Test_images',  # This is the source directory for training images
        target_size=(32, 32),  # All images will be resized to 32x32
        batch_size=1,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='categorical')


classes= ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#print(Xnew)
dirr='/content/Test_images3/Test_images3/Test_images/frog'
test_images=os.listdir('/content/Test_images3/Test_images3/Test_images/frog')
all_image_array=[]
images_new=[]
for i in test_images: all_image_array.append(img_to_array(load_img(dirr+'/'+i)))#Image has been saved\
for j in all_image_array:
    j=j/255
    #print(j)
    plt.imshow(j)
    #j = rescale(j, 0.25, anti_aliasing=False)
    j = resize(j, (32, 32), anti_aliasing=True)
    images_new.append(j)
print(np.array(images_new).shape)
x = np.reshape(np.array(images_new), (np.array(images_new).shape[0], -1))
ynew = svc.predict(x)    #model.predict_classes(np.array(images_new))
print(ynew)
for i in range(9):
    # define subplot
        plt.subplot(330 + 1 + i)
    # plot raw pixel data
        plt.title(classes[ynew[i]])
        plt.imshow(images_new[i])
    # show the figure

"""## SVM Polynomial Kernel"""

acc_train_svm_poly = []
acc_test_svm_poly = []

def svm_polynomial(c):

    svc_polynomial = svm.SVC(probability = False, kernel = 'poly', C = c)
    
    
    svc_polynomial.fit(xTrain, yTrain) 
    
    # Find the prediction and accuracy on the training set.
    Yhat_svc_polynomial_train = svc_polynomial.predict(xTrain)
    acc_train = np.mean(Yhat_svc_polynomial_train == yTrain)
    acc_train_svm_poly.append(acc_train)
    print('Accuracy = {0:f}'.format(acc_train))
    
    # Find the prediction and accuracy on the test set.
    Yhat_svc_polynomial_test = svc_polynomial.predict(xVal)
    acc_test = np.mean(Yhat_svc_polynomial_test == yVal)
    acc_test_svm_poly.append(acc_test)
    print('Accuracy = {0:f}'.format(acc_test))

c_svm_poly = [0.0001,0.001,0.01,0.1,1,10,100]


for c in c_svm_poly:
    svm_polynomial(c)

plt.plot(c_svm_poly, acc_train_svm_poly,'.-',color='red')
plt.plot(c_svm_poly, acc_test_svm_poly,'.-',color='orange')
plt.xlabel('c')
plt.ylabel('Accuracy')
plt.title("Plot of accuracy vs c for training and test data")
plt.grid()

#Try more values of c for polynomial kernel.
c_svm_poly_extended=[200,500,1000]
for c in c_svm_poly_extended:
    svm_polynomial(c)

"""## SVM RBF Kernel"""

def svm_rbf(c, g):
    svc_rbf = svm.SVC(probability = False, kernel = 'rbf', C = c, gamma = g)
    
    # Fit the classifier on the training set.
    svc_rbf.fit(xTrain, yTrain) 
    
    # Find the prediction and accuracy on the training set.
    Yhat_svc_rbf_train = svc_rbf.predict(xTrain)
    acc = np.mean(Yhat_svc_rbf_train == yTrain)
    print('Train Accuracy = {0:f}'.format(acc))
    acc_train_svm_rbf.append(acc)
    
    # Find the prediction and accuracy on the test set.
    Yhat_svc_rbf_test = svc_rbf.predict(xVal)
    acc = np.mean(Yhat_svc_rbf_test == yVal)
    print('Test Accuracy = {0:f}'.format(acc))
    acc_test_svm_rbf.append(acc)

acc_train_svm_rbf= []
acc_test_svm_rbf = []
c_svm_rbf = [0.0001,0.001,0.01,0.1,1,10,100]

for c in c_svm_rbf:
     svm_rbf(c, 'auto')
    
plt.plot(c_svm_rbf, acc_train_svm_rbf,'.-',color='red')
plt.plot(c_svm_rbf, acc_test_svm_rbf,'.-',color='orange')
plt.xlabel('c')
plt.ylabel('Accuracy')
plt.title("Plot of accuracy vs c for training and test data")
plt.grid()

"""## SUMMARIZING RESULTS FOR THE 3 KERNELS"""

# for i in range(len(acc_train_svm_linear)): 
#     acc_train_svm_linear[i]=round(acc_train_svm_linear[i],3)
#     acc_test_svm_linear[i]=round(acc_test_svm_linear[i],3)
#     acc_train_svm_poly[i]=round(acc_train_svm_poly[i],3)
#     acc_test_svm_poly[i]=round(acc_test_svm_poly[i],3)
#     acc_train_svm_rbf[i]=round(acc_train_svm_rbf[i],3)
#     acc_test_svm_rbf[i]=round(acc_test_svm_rbf[i],3)
    

    
print("SVM Linear Training Accuracy = ", acc_train_svm_linear)
print("SVM Linear Test Accuracy = ", acc_test_svm_linear)
print("SVM Polynomial Training Accuracy = ", acc_train_svm_poly)
print("SVM Polynomial Test Accuracy = ", acc_test_svm_poly)
print("SVM RBF Training Accuracy = ", acc_train_svm_rbf)
print("SVM RBF Test Accuracy = ", acc_test_svm_rbf)

"""## BEST MODEL (LINEAR KERNEL WITH C=0.1)"""

#Train with 10000 examples with linear kernel (c=0.1)

# Load the CIFAR10 dataset
from keras.datasets import cifar10
baseDir = os.path.dirname(os.path.abspath('__file__')) + '/'
classesName = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
(xTrain, yTrain), (xTest, yTest) = cifar10.load_data()
xVal = xTrain[49000:, :].astype(np.float)
yVal = np.squeeze(yTrain[49000:, :])
xTrain = xTrain[:49000, :].astype(np.float)
yTrain = np.squeeze(yTrain[:49000, :])
yTest = np.squeeze(yTest)
xTest = xTest.astype(np.float)

print(xTrain.shape)
print(yTrain.shape)
xTrain = np.reshape(xTrain, (xTrain.shape[0], -1)) # The -1 means that the corresponding dimension is calculated from the other given dimensions.
xVal = np.reshape(xVal, (xVal.shape[0], -1))
xTest = np.reshape(xTest, (xTest.shape[0], -1))
print(xTrain.shape) 
print(xTrain[0])

#Normalize
xTrain=((xTrain/255)*2)-1 
print(xTrain.shape)
print(xTrain[0])

xTrain=xTrain[:10000,:]
yTrain=yTrain[:10000]
print(yTrain)
print(xTrain.shape)
print(yTrain.shape)

from sklearn import svm
svc = svm.SVC(probability = False, kernel = 'linear', C = 0.1)
svc.fit(xTrain, yTrain)

Yhat_svc_linear_test = svc.predict(xVal)
acc_test = np.mean(Yhat_svc_linear_test == yVal)
print('Test Accuracy = {0:f}'.format(acc_test))

def plt_img(x):
    nrow = 32
    ncol = 32
    ncolors=3
    xsq = x.reshape((nrow,ncol,ncolors))
    plt.imshow(xsq)
#     plt.xticks([])
#     plt.yticks([])

#Plotting some of the errors
Ierr = np.where((Yhat_svc_linear_test != yVal))[0]
nplt = 4
plt.figure(figsize=(10, 4))
for i in range(nplt):        
    plt.subplot(1,nplt,i+1)        
    ind = Ierr[i]    
    plt_img(xVal[ind,:])        
    title = 'true={0:s} est={1:s}'.format(classesName[yVal[ind].astype(int)], classesName[Yhat_svc_linear_test[ind].astype(int)])
    plt.title(title)

"""## Without Normalization (using original pixel values 0-255)"""

# Commented out IPython magic to ensure Python compatibility.
import os
import time
import numpy as np


import matplotlib.pyplot as plt
import matplotlib as mpl
# %matplotlib inline


# Load the CIFAR10 dataset
from keras.datasets import cifar10
baseDir = os.path.dirname(os.path.abspath('__file__')) + '/'
classesName = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
(xTrain, yTrain), (xTest, yTest) = cifar10.load_data()
xVal = xTrain[49000:, :].astype(np.float)
yVal = np.squeeze(yTrain[49000:, :])
xTrain = xTrain[:49000, :].astype(np.float)
yTrain = np.squeeze(yTrain[:49000, :])
yTest = np.squeeze(yTest)
xTest = xTest.astype(np.float)

print(xTrain.shape)
print(yTrain.shape)
xTrain = np.reshape(xTrain, (xTrain.shape[0], -1)) # The -1 means that the corresponding dimension is calculated from the other given dimensions.
xVal = np.reshape(xVal, (xVal.shape[0], -1))
xTest = np.reshape(xTest, (xTest.shape[0], -1))
print(xTrain.shape) 
print(xTrain[0])

# #Normalize 
# xTrain=((xTrain/255)*2)-1 
# print(xTrain.shape)
# print(xTrain[0])

#Running SVM 
xTrain=xTrain[:10000,:]
yTrain=yTrain[:10000]
print(yTrain)
print(xTrain.shape)
print(yTrain.shape)
from sklearn import svm
svc = svm.SVC(probability=False,  kernel="linear", C=0.1)
svc.fit(xTrain, yTrain)

Yhat_svc_linear_test = svc.predict(xVal)
acc_test = np.mean(Yhat_svc_linear_test == yVal)
print('Test Accuracy = {0:f}'.format(acc_test))

"""## With Mean Normalization"""

# Commented out IPython magic to ensure Python compatibility.
import os
import time
import numpy as np


import matplotlib.pyplot as plt
import matplotlib as mpl
# %matplotlib inline


# Load the CIFAR10 dataset
from keras.datasets import cifar10
baseDir = os.path.dirname(os.path.abspath('__file__')) + '/'
classesName = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
(xTrain, yTrain), (xTest, yTest) = cifar10.load_data()
xVal = xTrain[49000:, :].astype(np.float)
yVal = np.squeeze(yTrain[49000:, :])
xTrain = xTrain[:49000, :].astype(np.float)
yTrain = np.squeeze(yTrain[:49000, :])
yTest = np.squeeze(yTest)
xTest = xTest.astype(np.float)


meanImage = np.mean(xTrain, axis=0)
print(meanImage.shape)
print('---------------------')
xTrain -= meanImage
xVal -= meanImage
xTest -= meanImage



print(xTrain.shape)
print(yTrain.shape)
xTrain = np.reshape(xTrain, (xTrain.shape[0], -1)) # The -1 means that the corresponding dimension is calculated from the other given dimensions.
xVal = np.reshape(xVal, (xVal.shape[0], -1))
xTest = np.reshape(xTest, (xTest.shape[0], -1))
print(xTrain.shape) 
print(xTrain[0])



#Running SVM 
xTrain=xTrain[:10000,:]
yTrain=yTrain[:10000]
print(yTrain)
print(xTrain.shape)
print(yTrain.shape)
from sklearn import svm
svc = svm.SVC(probability=False,  kernel="linear", C=0.1)
svc.fit(xTrain, yTrain)

Yhat_svc_linear_test = svc.predict(xVal)
acc_test = np.mean(Yhat_svc_linear_test == yVal)
print('Test Accuracy = {0:f}'.format(acc_test))

#GIVES BEST ACCURACY WITH DATA AUGMENTATION AND REGULARIZATION VGG-3
import keras
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.datasets import cifar10
from keras import regularizers
from keras.callbacks import LearningRateScheduler
import numpy as np
from sklearn.svm import SVC
 
def lr_schedule(epoch):
    lrate = 0.001
    if epoch > 75:
        lrate = 0.0005
    if epoch > 100:
        lrate = 0.0003
    return lrate
 
(x_train, y), (x_test, y_test) = cifar10.load_data()
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
 
#z-score
mean = np.mean(x_train,axis=(0,1,2,3))
std = np.std(x_train,axis=(0,1,2,3))
x_train = (x_train-mean)/(std+1e-7)
x_test = (x_test-mean)/(std+1e-7)
 
num_classes = 10
y_train = np_utils.to_categorical(y,num_classes)
y_test = np_utils.to_categorical(y_test,num_classes)
 
weight_decay = 1e-4
model = Sequential()
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay), input_shape=x_train.shape[1:]))
w1=model.get_weights()
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(32, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))
 
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.3))
 
model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3,3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))
 
model.add(Flatten())
w=model.get_weights()
o=model.output
model.add(Dense(num_classes, activation='linear')) #softmax

model.summary()
 
#data augmentation
datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    )
datagen.fit(x_train)
ypred = model.predict_classes(x_train) 
#training
batch_size = 32
 
opt_rms = keras.optimizers.rmsprop(lr=0.001,decay=1e-6)  #categorical_crossentropy
model.compile(loss='hinge', optimizer=opt_rms, metrics=['accuracy'])
model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),\
                    steps_per_epoch=x_train.shape[0] // batch_size,epochs=150,\
                    verbose=1,validation_data=(x_test,y_test),callbacks=[LearningRateScheduler(lr_schedule)])
#weights = l.get_weights()

#save to disk
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)
model.save_weights('model.h5') 

'''
scores = model.evaluate(x_test, y_test, batch_size=128, verbose=1)
print('\nTest result: %.3f loss: %.3f' % (scores[1]*100,scores[0])
'''

import matplotlib.pyplot as plt

plt.plot(model.history.history['accuracy'])
plt.plot(model.history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(model.history.history['loss'])
plt.plot(model.history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()