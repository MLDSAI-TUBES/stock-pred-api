import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler

class NormalizeFeatures(object):
    def __init__(self, df):
        self.df = df
        self.scaledDF = self.scaledDF()
    
    def scaledDF(self):
        with open('./scalers/scalers.obj', 'rb') as fh:
            scalers = pickle.load(fh)

        scaled_MAs = scalers['MAs'].fit_transform(self.df[['7 DAYS MA', '14 DAYS MA', '21 DAYS MA']])
        scaled_std = scalers['std'].fit_transform(self.df[['7 DAYS STD DEV']])
        scaled_dow = scalers['dow'].fit_transform(self.df[['dayofweek']])
        scaled_q = scalers['q'].fit_transform(self.df[['quarter']])
        scaled_m = scalers['m'].fit_transform(self.df[['month']])
        scaled_y = scalers['y'].fit_transform(self.df[['year']])
        scaled_doy = scalers['doy'].fit_transform(self.df[['dayofyear']])
        scaled_dom = scalers['dom'].fit_transform(self.df[['dayofmonth']])
        scaled_woy = scalers['woy'].fit_transform(self.df[['weekofyear']])

        df_normalized = pd.DataFrame(scaled_MAs)
        df_normalized.index = self.df.index
        df_normalized['7 DAYS STD DEV'] = scaled_std
        df_normalized['dayofweek'] = scaled_dow
        df_normalized['quarter'] = scaled_q
        df_normalized['month'] = scaled_m
        df_normalized['year'] = scaled_y
        df_normalized['dayofyear'] = scaled_doy
        df_normalized['dayofmonth'] = scaled_dom
        df_normalized['weekofyear'] = scaled_woy

        df_normalized.rename(columns={0:'7 DAYS MA', 1:'14 DAYS MA', 2:'21 DAYS MA'}, inplace = True)

        return df_normalized

    def getScaledDF(self):
        return self.scaledDF

