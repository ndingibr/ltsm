
import os
import json
import time
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from core.data_processor import data_processor
from core.plots import plots
from core.features import features
from core.model import model
import datetime as dt
from fbprophet import Prophet


def plot_results(actual, predicted, trade):
    plt.plot(actual, color = 'black', label = 'Actual Stock Price')
    plt.plot(predicted, color = 'green', label = 'Predicted Stock Price')
    title = ''.join(trade) + 'Stock Price Prediction'
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('bANGJ Stock Price')
    plt.legend()
    plt.show()

def main():
    
    df = pd.read_csv('NSE-TATAGLOBAL11.csv')
    #print(df.head())
    
    #setting index as date
    df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
    df.index = df['Date']

    data = df.sort_index(ascending=True, axis=0)
    #creating dataframe
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
    
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]
    
    new_data['Date'] = pd.to_datetime(new_data.Date,format='%Y-%m-%d')
    new_data.index = new_data['Date']
    
    #preparing data
    new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)
    
    #train and validation
    train = new_data[:1230]
    valid = new_data[1230:]
    
    #fit the model
    model = Prophet()
    model.fit(train)
    
    close_prices = model.make_future_dataframe(periods=len(valid))
    forecast = model.predict(close_prices)
    
    #rmse
    forecast_valid = forecast['yhat'][1230:]
    rms=np.sqrt(np.mean(np.power((np.array(valid['y'])-np.array(forecast_valid)),2)))
    print(rms)
    
    #plot
    valid['Predictions'] = 0
    valid['Predictions'] = forecast_valid.values
    
    plt.plot(train['y'])
    plt.plot(valid[['y', 'Predictions']])
         
if __name__ == '__main__':
    main()