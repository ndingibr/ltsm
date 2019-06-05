import os
import json
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from core.data_processor import data_processor
from core.model import model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score


def main():
    
    configs = json.load(open('config.json', 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    
    file_path = os.path.join('data', configs['data']['filename'])
    connection = os.path.join(configs['data']['postgres_connection'])
        
    processor = data_processor(file_path, connection)
    
    test_end_date = configs['training']['test_end_date']
    table_name = configs['data']['table_name']
    metric_table = configs['data']['metric_table']
    
    raw_data = processor.get_data()

    closes = ['EUR/USD Close', 'USD/JPY Close', 'USD/CHF Close', 'GBP/USD Close', 'USD/CAD Close', 'EUR/GBP Close', 'EUR/JPY Close', 'EUR/CHF Close',  'AUD/USD Close', 'GBP/JPY Close', 'CHF/JPY Close',  'GBP/CHF Close',  'NZD/USD Close']
    
    processor.check_table(table_name)
    processor.create_tables(table_name)
    
    processor.check_table(metric_table)
    processor.create_metrictable(metric_table)
    
    all_tests = pd.DataFrame()
    metrics = pd.DataFrame(pd.DataFrame(columns=['Date','Trade','RMSE','RSquared','Increase_Pecentage', 'Increase_PecentageActual']))
    
    
    start = True 
    
    for trade in closes:
        print(trade)
        df = raw_data[['Date', trade]]
        min_date = df['Date'].min()
                
        df = processor.get_data_in_range(df, min_date, test_end_date)
        
        print(len(df))
        
        df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
        df.index = df['Date']
    
        data = df.sort_index(ascending=True, axis=0)
        new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', trade])
        for i in range(0,len(data)):
            new_data['Date'][i] = data['Date'][i]
            new_data[trade][i] = data[trade][i]
    
        #setting index
        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)
    
        #creating train and test sets
        dataset = new_data.values
        
        split_index = len(df) - 5
        
        train = dataset[0:split_index,:]
        valid = dataset[split_index:,:]
    
        #converting dataset into x_train and y_train
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(train)
              
        x_train, y_train = [], []
        for i in range(60,len(train)):
            x_train.append(scaled_data[i-60:i,0])
            y_train.append(scaled_data[i,0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        print(x_train.shape)
        
        x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
        
        model_result = model(x_train, y_train)
        lstm_model = model_result.lstm_keras()
        
        begin_index = len(df) - 70
        end_index = len(df) - 5
        
        inputs = dataset[begin_index:split_index,:]
        scaler_input = MinMaxScaler(feature_range=(0, 1))
        scaled_input = scaler_input.fit_transform(inputs)
        print(len(inputs))
        
        X_test = []
        for i in range(0, 5):
            X_test.append(scaled_input[i:i + 60,0])
        X_test = np.array(X_test)
        print(X_test.shape)
        
        
        X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
        closing_price = lstm_model.predict(X_test)
        closing_price = scaler.inverse_transform(closing_price)
        
        
        #rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
        #print(rms)
        
        valid = new_data[end_index:]
        print(valid)
        valid['Predictions'] = closing_price
        #plt.plot(train[trade])
        #plt.plot(valid[[trade,'Predictions']])
        #plt.show()
        
        latest_test_set = df.tail(5)
        latest_test_set = latest_test_set.copy()
        
        #min = latest_test_set[trade].ix[0]
        #max = latest_test_set[trade].ix[len(latest_test_set) - 1]
        
        #actual_change = (max - min)/min
        
        if start == True:
            all_tests['Date'] = latest_test_set['Date']
        
        all_tests[trade] = closing_price
        start = False  
        
        rsquared = r2_score(latest_test_set[trade], closing_price)
        
        print(all_tests)
        print('Min = ' + str(all_tests[trade].ix[0]))
        print('Max = ' + str(all_tests[trade].ix[len(latest_test_set) - 1]))
        
        min = all_tests[trade].ix[0]
        max = all_tests[trade].ix[len(latest_test_set) - 1]
        
        change = (max - min)/min
       
        metrics = metrics.append({'Date': datetime.datetime.now(), 'Trade': trade, 'RMSE': 0, 'RSquared': 0, 'Increase_Pecentage' : change, 'Increase_PecentageActual' : 0}, ignore_index=True)
        
    print(all_tests)
    processor.save_csv(os.path.join('data', configs['data']['predictions_filename']), all_tests)
    processor.load_table_cv(os.path.join('data', configs['data']['predictions_filename']), table_name)
    
    processor.save_csv(os.path.join('data', configs['data']['filename_metrics']), metrics)
    processor.load_table_cv(os.path.join('data', configs['data']['filename_metrics']), metric_table)
        
    print('done')

if __name__ == '__main__':
    main()