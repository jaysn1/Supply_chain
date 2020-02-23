from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyoff
import os, sqlite3

def render_plot(time, selected_store, selected_product):
    con = sqlite3.connect('site.db')
    cur = con.cursor()
    cur.execute('SELECT purchase_date as data,sale_sum as sales FROM sales where product_id = {} and store_id = {};'.format(selected_product, selected_store))
    #series = pd.read_csv(os.getcwd() + "/flasksite/data/sales_data{}_{}.csv".format(selected_store,selected_product))
    #convert date field from string to datetime
    rows = cur.fetchall()
    series = []
    for row in rows:
        series.append(list(row))
    series = pd.DataFrame(series, columns = ["date","sales"])

    series['date'] = pd.to_datetime(series['date'])


    #represent month in date field as its first day
    series['date'] = series['date'].dt.year.astype('str') + '-' + series['date'].dt.month.astype('str') + '-01'
    series['date'] = pd.to_datetime(series['date'])
    #groupby date and sum the sales
    series = series.groupby('date').sales.sum().reset_index()

    #series = read_csv('sales_data1.csv')
    X = series['sales']
    #X = series.values
    #size = int(len(X) * 0.66)
    train = X
    history = [x for x in train]
    #    number = int(input("How many months of predictions you want:"))
    number = time
    dates = []
    for i in range(number):
        dates.append(datetime(2018, i+1, 1))
        

    predictions = list()
    for t in range(number):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0][0]
        predictions.append(yhat)
        obs = yhat
        history.append(obs)
    #	print('predicted=%f, expected=%f' % (yhat, obs))
    #error = mean_squared_error(test, predictions)
    #print('Test MSE: %.3f' % error)
    plot_data = [
        go.Scatter(
            x=series['date'],
            y=series['sales'],
            name='actual'
        ),
            go.Scatter(
            x=dates,
            y=predictions,
            name='predicted'
        )
        
    ]
    plot_layout = go.Layout(
            title='Sales Prediction'
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    pyoff.plot(fig, filename=os.getcwd() + '/flasksite/templates/temp-plot.html', auto_open=False)