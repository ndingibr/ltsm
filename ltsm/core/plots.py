from plotly import tools
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, iplot, iplot_mpl

class plots(object):

    def __init__(self, train, test):
        """Returns the model"""
        self.train = train
        self.test = test

    def plot_train_test(self, date_split):   
        
        data = [
            Candlestick(x=self.train.index, open=self.train['Open'], high=self.train['High'], low=self.train['Low'], close=self.train['Price'], name='train'),
            Candlestick(x=self.test.index, open=self.test ['Open'], high=self.test ['High'], low=self.test ['Low'], close=self.test ['Price'], name='test')
        ]
        layout = {
             'shapes': [
                 {'x0': date_split, 'x1': date_split, 'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper', 'line': {'color': 'rgb(0,0,0)', 'width': 1}}
             ],
            'annotations': [
                {'x': date_split, 'y': 1.0, 'xref': 'x', 'yref': 'paper', 'showarrow': False, 'xanchor': 'left', 'text': ' test data'},
                {'x': date_split, 'y': 1.0, 'xref': 'x', 'yref': 'paper', 'showarrow': False, 'xanchor': 'right', 'text': 'train data '}
            ]
        }
        figure = Figure(data=data, layout=layout)
        iplot(figure)
     