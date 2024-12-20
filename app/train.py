import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import time
import mlflow
import mlflow.keras

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, Input
from keras.utils import to_categorical

# set mlflow
mlflow.set_experiment('mnist-experiment')

# Importation de données via keras
mnist = keras.datasets.mnist
(x_train,y_train),(x_test,y_test) = mnist.load_data()
#print('\n train_x:%s, train_y:%s, test_x:%s, test_y:%s'%(x_train.shape,y_train.shape,x_test.shape,y_test.shape))

# Prétraitement des données
X_train4D = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
X_test4D = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32')

X_train4D_Normalize = X_train4D / 255 #  normalisation
X_test4D_Normalize = X_test4D / 255

y_trainOnehot = to_categorical(y_train)
y_testOnehot = to_categorical(y_test)

# Lancer mlflow
with mlflow.start_run():


    # Modélisation
    model = Sequential()

    model.add(Input(shape=(28, 28, 1)))

    ## 1ère couche de convolution
    model.add(Conv2D(filters=16, kernel_size=(5, 5), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))  # 1ère couche d'accumulation / Max poolling
    model.add(Dropout(0.25))

    ## 2ème couche de convolution
    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))  # 2ème couche d'accumulation / Max poolling
    model.add(Dropout(0.25))

    ## Plus de convolution layers
    model.add(Conv2D(filters=64, kernel_size=(5, 5), padding='same', activation='relu'))
    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    ## Flatten + Dense layers
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(10, activation='softmax'))

    ## Afficher le résumé du modèle
    #print(model.summary())

    # Configurer la méthode d'apprentissage du modèle¶
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    # log de modele avec mlflow
    mlflow.log_param("epochs", 10)
    mlflow.log_param("batch_size", 300)
    mlflow.log_param("optimizer", 'adam')

    # Entraîner le modèle
    #print('------------')
    #nowtime = time.strftime('%d-%m-%Y %H:%M:%S')
    #print('Commencer à '+str(nowtime))

    train_history = model.fit(x=X_train4D_Normalize,
                            y=y_trainOnehot,
                            validation_split=0.2,
                            batch_size=300,
                            epochs=10,
                            verbose=2)

    # Log de metrics avec MLflow
    mlflow.log_metric("final_loss", train_history.history['loss'][-1])
    mlflow.log_metric("final_accuracy", train_history.history['accuracy'][-1])

    #print('------------')
    #nowtime = time.strftime('%d-%m-%Y %H:%M:%S')
    #print('Terminer à '+str(nowtime))

    # Evaluer modèle
    #model.evaluate(X_test4D_Normalize,y_testOnehot)
    test_loss, test_acc = model.evaluate(X_test4D_Normalize, y_testOnehot)
    mlflow.log_metric("test_loss", test_loss)
    mlflow.log_metric("test_accuracy", test_acc)

    # Enregistrer modèle
    #model.save('save/modelMnist1.keras')
    mlflow.keras.log_model(model, "model")

    # Visibilisation le resultat
    #print(train_history.history)
    loss = train_history.history['loss']
    val_loss = train_history.history['val_loss']
    acc = train_history.history['accuracy']
    val_acc = train_history.history['val_accuracy']

    plt.figure(figsize=(10,3))

    plt.subplot(121)
    plt.plot(loss,color='b',label='train')
    plt.ylabel('loss')
    plt.legend()

    plt.subplot(122)
    plt.plot(acc,color='b',label='train')
    plt.plot(val_acc,color='r',label='test')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.figure()
    for i in range(10):
        num = np.random.randint(1,10000)

        plt.subplot(2,5,i+1)
        plt.axis('off')
        plt.imshow(x_test[num],cmap='gray')
        demo = tf.reshape(X_test4D_Normalize[num],(1,28,28))
        y_pred = np.argmax(model.predict(demo))
        plt.title('Label: '+str(y_test[num])+'\nPredict: '+str(y_pred))

    plt.show()