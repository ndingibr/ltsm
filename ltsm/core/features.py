from sklearn.preprocessing import MinMaxScaler
time_step = 60
import numpy as np

class features(object):
 
    def feature_scaling(data_set):
        sc = MinMaxScaler(feature_range = (0, 1))
        data_set_scaled = sc.fit_transform(data_set)
        return data_set_scaled
    
    def data_timesteps(set_scaled):
        X_train = []
        y_train = []
        for i in range(time_step, len(set_scaled)):
            X_train.append(set_scaled[i-time_step:i, 0])
            y_train.append(set_scaled[i, 0])
            X_train, y_train = np.array(X_train), np.array(y_train)
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            return y_train, X_train
