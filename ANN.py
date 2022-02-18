# -*- coding: utf-8 -*-
"""Aritificial_Neural_Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZFbO8etqJmvtfurACtP47PEPz5o95LsF
"""

!pip install Cython
!pip install https://github.com/Santosh-Gupta/scikit-learn/archive/master.zip

import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score

dataset = pd.read_csv('Churn_Modelling.csv')
x = dataset.iloc[:, 3:-1]
y = dataset.iloc[:, -1]

# Encoding "Gender"
le = LabelEncoder()
x.iloc[:, 2] = le.fit_transform(x.iloc[:, 2])

# Enconding "Geography"
x.iloc[:, 1] = le.fit_transform(x[["Geography"]])# As a result, we have: France = 0; Germay = 1; Spain = 2
x

# Define training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

# Feature scaling
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Create our Aritificial Neural Network (ANN)
ann = tf.keras.models.Sequential()

# Add input layer and first hidden layer to ANN
ann.add(tf.keras.layers.Dense(units = 6, activation = 'relu'))

# Add second layer
ann.add(tf.keras.layers.Dense(units = 6, activation = 'relu'))

# Add the output layer
ann.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

# Compile ANN
ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Train ANN on Training set
ann.fit(x_train, y_train, batch_size = 32, epochs = 100)

# Predict if the costumer with the following informations will leave the bank:
#    Greography: France
#    Credit Score: 600
#    Gender: Male
#    Age: 40 years old
#    Tenure: 3 years
#    Balance: $ 60000
#    Have a credit card: yes
#    Is it an active member: yes
#    Estimated salary: $ 50000
print(ann.predict(sc.transform([[0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])) > 0.5)

# Predict the Test set results
y_pred = ann.predict(x_test)
y_pred = y_pred > 0.5
y_test = np.array(y_test)
print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1))

# Make the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)