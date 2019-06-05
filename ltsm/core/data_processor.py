import psycopg2
import pandas as pd
import datetime as dt

class data_processor():
    """A class for loading and transforming data for the lstm model"""

    def __init__(self, filename, connection):
        self.filename = filename
        self.connection = psycopg2.connect(connection)
        
    def get_data(self):
        return pd.read_csv(self.filename)

    def get_trades_by_range(self, ending_date):
        print(type(ending_date))
        cursor = self.connection.cursor()
        postgreSQL_select_query = '''
        	SELECT p.date, e."EUR/GBP Close", p."EUR/GBP Close"
        	FROM public.predictions p 
        	join public.exchange e on
        	p.date = e.date where p.date > ''' 
        print(postgreSQL_select_query)
        postgreSQL_select_query = postgreSQL_select_query + "'" + ending_date + "'"
        cursor.execute(postgreSQL_select_query)
        closes = pd.DataFrame(cursor.fetchall(), columns=['date', 'actual', 'predicted'])
        return closes
    
    def get_trades(self):
        """Returns all the trades from the database that can be analysed"""
        cursor = self.connection.cursor()
        postgreSQL_select_query = "select code from trade"
        cursor.execute(postgreSQL_select_query)
        trades = cursor.fetchall() 
        return trades
    
    def check_table(self, table_name):
        cursor = self.connection.cursor()
        query = "drop table if exists " + table_name
        cursor.execute(query)
        print('drop done')

    def get_data_in_range(self, data_set, starting_date, ending_date):
        # Convert to date field to be able to filter by dates
        data_set['Date'] = pd.to_datetime(data_set['Date'])
        set_filtered = data_set[(data_set['Date'] <= ending_date)]
        set_filtered = set_filtered[(set_filtered['Date'] >= starting_date)]
        return set_filtered
    
    
    def create_tables(self, table_name):
        cursor = self.connection.cursor()
        
        create_table_query = 'CREATE TABLE ' +  table_name
        create_table_query = create_table_query + '''
        (
                Date date,
                "EUR/USD Close" numeric, 
                "USD/JPY Close" numeric, 
                "USD/CHF Close" numeric, 
                "GBP/USD Close" numeric, 
                "USD/CAD Close" numeric, 
                "EUR/GBP Close" numeric, 
                "EUR/JPY Close" numeric, 
                "EUR/CHF Close" numeric,  
                "AUD/USD Close" numeric, 
                "GBP/JPY Close" numeric, 
                "CHF/JPY Close" numeric,  
                "GBP/CHF Close" numeric,  
                "NZD/USD Close" numeric
        ); '''
        
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_metrictable(self, table_name):
        cursor = self.connection.cursor()
        
        create_table_query = 'CREATE TABLE ' +  table_name
        create_table_query = create_table_query + '''
        (
                Date date,
                "Trade" varchar, 
                "RMSE" numeric, 
                "RSquared" numeric, 
                "Increase_Pecentage" numeric,
                "Increase_PecentageActual" numeric
 
        ); '''
        
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_exchangetable(self, table_name):
        cursor = self.connection.cursor()
        
        create_table_query = 'CREATE TABLE ' +  table_name
        create_table_query = create_table_query + '''
        (
                date date,
                "EUR/USD Close"  numeric,
                "EUR/USD High" numeric,
                "EUR/USD Low" numeric,
                "USD/JPY Close" numeric,
                "USD/JPY High" numeric,
                "USD/JPY Low" numeric,
                "USD/CHF Close"  numeric,
                "USD/CHF High"  numeric,
                "USD/CHF Low"  numeric,
                "GBP/USD Close"  numeric,
                "GBP/USD High"  numeric,
                "GBP/USD Low" numeric,
                "USD/CAD Close" numeric,
                "USD/CAD High" numeric,
                "USD/CAD Low" numeric,
                "EUR/GBP Close" numeric,
                "EUR/GBP High" numeric,
                "EUR/GBP Low" numeric,
                "EUR/JPY Close" numeric,
                "EUR/JPY High" numeric,
                "EUR/JPY Low" numeric,
                "EUR/CHF Close" numeric,
                "EUR/CHF High" numeric,
                "EUR/CHF Low" numeric,
                "AUD/USD Close" numeric,
                "AUD/USD High" numeric,
                "AUD/USD Low" numeric,
                "GBP/JPY Close" numeric,
                "GBP/JPY High" numeric,
                "GBP/JPY Low" numeric,
                "CHF/JPY Close" numeric,
                "CHF/JPY High" numeric,
                "CHF/JPY Low" numeric,
                "GBP/CHF Close" numeric,
                "GBP/CHF High" numeric,
                "GBP/CHF Low" numeric,
                "NZD/USD Close" numeric,
                "NZD/USD High" numeric,
                "NZD/USD Low" numeric
        ); '''
        
        print(create_table_query)
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def save_csv(self, file_name, data_frame):
        data_frame.to_csv(file_name, index=False)
    
    def insert_records(self, file_name, table_name, records):
        cursor = self.connection.cursor()
        query = 'insert into ' + table_name + ''' (date, "EUR/USD Close", "USD/JPY Close", "USD/CHF Close", "GBP/USD Close", "USD/CAD Close", "EUR/GBP Close", "EUR/JPY Close", "EUR/CHF Close", "AUD/USD Close", "GBP/JPY Close", "CHF/JPY Close", "GBP/CHF Close", "NZD/USD Close") ''' + 'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)'
        cursor.close()
    
    def load_table_cv(self, file_path, table_name):
        cursor = self.connection.cursor()
        
        with open(file_path, 'r') as f:

            next(f)  # Skip the header row.
            cursor.copy_from(f, table_name, sep=',')

        self.connection.commit()
        cursor.close()
        print('table copied')
