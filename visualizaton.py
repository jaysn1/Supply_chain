# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 00:13:36 2020

@author: Jaysn
"""

from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd


#read the data in csv
series = pd.read_csv('sales_data2.csv')
#convert date field from string to datetime
series['date'] = pd.to_datetime(series['date'])


#represent month in date field as its first day
series['date'] = series['date'].dt.year.astype('str') + '-' + series['date'].dt.month.astype('str') + '-01'
series['date'] = pd.to_datetime(series['date'])
#groupby date and sum the sales
series = series.groupby('date').sales.sum().reset_index()

#series = read_csv('sales_data1.csv')
X = series['sales']
#X = series.values
size = int(len(X) * 0.50)
#train = X
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
#number = int(input("How many months of predictions you want:"))
#dates = []

#for i in range(number):
#    dates.append(datetime(2018, i+1, 1))
    

predictions = list()
for t in range(30,30+len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
#	print('predicted=%f, expected=%f' % (yhat, obs))
#error = mean_squared_error(test, predictions)
#print('Test MSE: %.3f' % error)
# plot
pyplot.plot(series['date'][:],X)
pyplot.plot(series['date'][-30:],predictions, color='red')
pyplot.show()