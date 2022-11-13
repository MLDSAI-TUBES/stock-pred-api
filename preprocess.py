import yfinance as yf
from datetime import date
import pandas as pd
import datetime

class PreprocessIndependentVariables(object):
    """
    Class to preprocess the independent variables from current date
    and given telecommunication company.
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.currDate = date.today()
        self.oneMoData = self.get1MoData()
        self.df = self.createDF()

    def get1MoData(self):
        try:
            oneMoData = yf.download(self.ticker, period='1mo')
        except:
            raise('Error in downloading historical stock data from yfinance')
        return oneMoData
    
    def generateMA(self, windowSize):
        try:
            closeSeries = self.oneMoData['Close']
            windows = closeSeries.rolling(windowSize)
            nDaysMA = 0
            dayNum = self.currDate.weekday()
            if dayNum < 5:
                nDaysMA = windows.mean()[-2]
            else:
                nDaysMA = windows.mean()[-1]
        except:
            raise(f'Error in calculating {windowSize} Days MA')

        return nDaysMA

    def generateStdDev(self, windowSize):
        try:
            closeSeries = self.oneMoData['Close']
            windows = closeSeries.rolling(windowSize)
            nDaysStdDev = 0
            dayNum = self.currDate.weekday()
            if dayNum < 5:
                nDaysStdDev = windows.std()[-2]
            else:
                nDaysStdDev = windows.mean()[-1]
        except:
            raise(f'Error in calculating {windowSize} Days Std Dev')

        return nDaysStdDev

    def createDF(self):
        try:
            data = {
                '7 DAYS MA': [self.generateMA(7)],
                '14 DAYS MA': [self.generateMA(14)],
                '21 DAYS MA': [self.generateMA(21)],
                '7 DAYS STD DEV': [self.generateStdDev(7)]
            }

            dayNum = self.currDate.weekday()
            if dayNum == 5:
                print('SATURDAY')
                # if current date is Saturday, predict the next Monday's price
                self.currDate = self.currDate + datetime.timedelta(days=2)
            elif dayNum == 6:
                print('SUNDAY')
                # if current date is Sunday, predict the next Monday's price
                self.currDate = self.currDate + datetime.timedelta(days=1)
                print(f'{self.currDate}')
            else:
                print(f'{self.currDate} WEEKDAY')

            df = pd.DataFrame(data=data)
            df['Date'] = [self.currDate]
            df = df.set_index('Date')
            df.index = pd.to_datetime(df.index)

            df['dayofweek'] = df.index.dayofweek
            df['quarter'] = df.index.quarter
            df['month'] = df.index.month
            df['year'] = df.index.year
            df['dayofyear'] = df.index.dayofyear
            df['dayofmonth'] = df.index.day
            df['weekofyear'] = df.index.isocalendar().week.astype('int32')
        except:
            raise('Error in creating DF')
        return df

    def getDF(self):
        return self.df