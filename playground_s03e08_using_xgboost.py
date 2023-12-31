# -*- coding: utf-8 -*-
"""Playground S03e08 using Xgboost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19Nnfffy1UvE6tP_M8B9lG-lEDU4EZvWD
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn import metrics

from xgboost import XGBRegressor

def model_evaluation(model,X_train,X_test,Y_train,Y_test):

    model.fit(X_train,Y_train)

    training_data_prediction = model.predict(X_train)
    testing_data_prediction  =  model.predict(X_test)

    r_sq_train = metrics.r2_score(Y_train, training_data_prediction)
    r_sq_test  = metrics.r2_score(Y_test, testing_data_prediction)
    rmse_train = np.sqrt(metrics.mean_squared_error(Y_train, training_data_prediction))
    rmse_test  = np.sqrt(metrics.mean_squared_error(Y_test, testing_data_prediction))

    print("R squared value of train data: ",r_sq_train)
    print("RMSE of train data: ",rmse_train)
    print("=========================================")
    print("R squared value of test data: ",r_sq_test)
    print("RMSE of test data: ",rmse_test)

    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    axs[0].scatter(Y_train, training_data_prediction)
    axs[0].set_title("Actual yield vs Predicted yield ( On training data)")
    axs[0].set_xlabel("Actual yield")
    axs[0].set_ylabel("Predicted yield")


    axs[1].scatter(Y_test, testing_data_prediction)
    axs[1].set_title("Actual yield vs Predicted yield (On testing data) ")
    axs[1].set_xlabel("Actual yield")
    axs[1].set_ylabel("Predicted yield")
    plt.show()

from google.colab import drive
drive.mount("/content/drive/",force_remount=True)

"""load and understand the data"""

dataset = pd.read_csv("/content/drive/MyDrive/Playground Dataset/train.csv")

dataset.shape

dataset.isnull().sum()

"""Data preprocessing (label endoce)"""

dataset['cut'].value_counts()

dataset['color'].value_counts()

dataset['clarity'].value_counts()

dataset.replace({'cut':{'Ideal':0, 'Premium':1, 'Very Good':2, 'Good':3, 'Fair':4}}, inplace=True)
dataset.replace({'color':{'G':0, 'E':1, 'F':2, 'H':3, 'D':4, 'I':5, 'J':6}}, inplace=True)
dataset.replace({'clarity':{'SI1':0, 'VS2':1, 'VS1':2, 'SI2':3, 'VVS2':4, 'VVS1':5, 'IF':6, 'I1':7}}, inplace=True)

dataset.rename(columns={"z": "Height"}, inplace=True)
dataset.rename(columns={"y": "Width"}, inplace=True)
dataset.rename(columns={"x": "Length"}, inplace=True)

dataset.head()

dataset['cut'].value_counts()

dataset['color'].value_counts()

dataset['clarity'].value_counts()

"""EDA"""

correlation = dataset.corr()

plt.figure(figsize=(10,10))
sns.heatmap(correlation, cbar=True, square=True, fmt='.1f', annot=True, annot_kws={'size':8}, cmap='Blues')

sns.countplot(x='cut', data=dataset)

sns.countplot(x='color', data=dataset)

sns.countplot(x='clarity', data=dataset)

sns.scatterplot(x='Length', y='price', data=dataset)
plt.xlim(3.4,9)

sns.scatterplot(x='Width', y='price', data=dataset)
plt.xlim(3.4,9)

sns.scatterplot(x='Height', y='price', data=dataset)
plt.xlim(2,5)

sns.scatterplot(x='carat', y='price', data=dataset)
plt.xlim(0,2.5)

sns.scatterplot(x='Length', y='carat', data=dataset)
plt.xlim(3.7,9)

sns.scatterplot(x='Width', y='carat', data=dataset)
plt.xlim(3.7,9)

sns.scatterplot(x='Height', y='carat', data=dataset)
plt.xlim(2,6)

"""Splitt data

"""

X = dataset.drop(columns=['price','id'], axis=1)

Y = dataset['price']

X.head()

Y.head()

X_train, X_test, Y_train, Y_test  = train_test_split(X, Y, test_size=0.25, random_state=10)

"""Model train and test"""

model1 = XGBRegressor()

model_evaluation(model1,X_train,X_test,Y_train,Y_test)

testDataset = pd.read_csv("/content/drive/MyDrive/Playground Dataset/test.csv")

testDataset.head()

id = testDataset['id']

testDataset.rename(columns={"z": "Height"}, inplace=True)
testDataset.rename(columns={"y": "Width"}, inplace=True)
testDataset.rename(columns={"x": "Length"}, inplace=True)

testDataset.replace({'cut':{'Ideal':0, 'Premium':1, 'Very Good':2, 'Good':3, 'Fair':4}}, inplace=True)
testDataset.replace({'color':{'G':0, 'E':1, 'F':2, 'H':3, 'D':4, 'I':5, 'J':6}}, inplace=True)
testDataset.replace({'clarity':{'SI1':0, 'VS2':1, 'VS1':2, 'SI2':3, 'VVS2':4, 'VVS1':5, 'IF':6, 'I1':7}}, inplace=True)

submissionTest = testDataset.drop(columns=['id'], axis=1)

submissionTest.head()

predictions = model1.predict(submissionTest)

submission_df = pd.DataFrame({'id': id, 'price': predictions})
submission_df.to_csv('submission.csv', index=False)

from google.colab import files

files.download('submission.csv')

import pickle

with open('predictor.pickle', 'wb') as file:
    pickle.dump(model_evaluation, file)