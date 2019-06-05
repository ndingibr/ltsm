from core.data_processor import data_processor


def upload_data():
    configs = json.load(open('config.json', 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    
    file_path = os.path.join('data', configs['data']['filename_exchange'])
    connection = os.path.join(configs['data']['postgres_connection'])
        
    processor = data_processor(file_path, connection)
    
    time_step = configs['training']['time_step']
    training_end_date = configs['training']['training_end_date']
    test_end_date = configs['training']['test_end_date']
    table_name = configs['data']['tablename_exchange']
    
    processor.check_table(table_name)
    
    processor.create_exchangetable(table_name)
    processor.load_table_cv(file_path, table_name)

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
    configs = json.load(open('config.json', 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    
    file_path = os.path.join('data', configs['data']['filename_exchange'])
    connection = os.path.join(configs['data']['postgres_connection'])
        
    processor = data_processor(file_path, connection)
    
    time_step = configs['training']['time_step']
    training_end_date = configs['training']['training_end_date']
    test_end_date = configs['training']['test_end_date']
    table_name = configs['data']['tablename_exchange']
            
    trades = processor.get_trades_by_range(training_end_date)
    print(trades)
    plot_results(trades['actual'], trades['predicted'], 'trade')

    
    print('done')
        
if __name__ == '__main__':
    main()