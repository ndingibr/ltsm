import os
import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


class model(object):
    """Trains the model based on X_train and y_train

    Attributes:
        X_train: training dataset.
        y_train: test dataset.
    """

    def __init__(self, X_train, y_train):
        """Returns the model"""
        self.X_train = X_train
        self.y_train = y_train

    def lstm_keras(self):
        # create and fit the LSTM network
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train.shape[1],1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))
        
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(self.X_train , self.y_train , epochs=1, batch_size=1, verbose=2)
        return model
    
    def prophet(self):
        model = Prophet()
        model.fit(data);
        future_stock_data = model.make_future_dataframe(periods=steps_ahead, freq = 'd')
        forecast_data = model.predict(future_stock_data)
         
        step_count=0
        # save actual data 
        for index, row in data_test.iterrows():
          
          results[ind][step_count][0] = row['y']
          results[ind][step_count][4] = row['ds']
          step_count=step_count + 1
         
        # save predicted data and calculate error
        count_index = 0  
        for index, row in forecast_data.iterrows():
          if count_index >= len(data)  :
             
             step_count= count_index - len(data)
             results[ind][step_count][1] = row['yhat']
             results[ind][step_count][2] = results[ind][step_count][0] -  results[ind][step_count][1]
             results[ind][step_count][3] = 100 * results[ind][step_count][2] / results[ind][step_count][0]
            
          count_index=count_index + 1

    def save_model(self, model, trade):
        configs = json.load(open('config.json', 'r'))
        directory = configs['model']['save_dir'] 
        model.save(directory + ''.join(trade) + ".h5")
    
    def test_set(test_set, training_set, model): 
        configs = json.load(open('config.json', 'r'))
        time_step = configs['training']['time_step']
        sc = MinMaxScaler(feature_range = (0, 1))
        training_set_scaled = sc.fit_transform(training_set)
        # Getting the real stock price of 2017

        real_stock_price = test_set
        inputs = test_set.reshape(-1,1)
        test_set_scaled = sc.transform(inputs)
        X_test = []
        for i in range(time_step, len(test_set_scaled)):
            X_test.append(test_set_scaled[i-time_step:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_stock_price = model.predict(X_test)
        return sc.inverse_transform(predicted_stock_price)