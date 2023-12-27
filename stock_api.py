#pip install alpha_vantage

#import necessary libraries
from alpha_vantage.timeseries import TimeSeries
from getpass import getpass
import requests
import pandas as pd

#configure API Key
API_key = getpass('API Key: ')

#set ticker
symbol = 'AAPL'

#get stock price history in a df format
ts = TimeSeries(key = API_key, output_format='pandas')
data = ts.get_intraday(symbol, interval='15min')

stock_price_df = data[0]

#get stock rsi history in a df format
url = 'https://www.alphavantage.co/query?function=RSI&symbol='+symbol+'&interval=15min&time_period=200&series_type=open&apikey=' + API_key
r = requests.get(url)
data = r.json()

stock_rsi_df = pd.json_normalize(data['Technical Analysis: RSI'])

#format data as desired
#transpose data to more useful form
stock_rsi_df_T = stock_rsi_df.T
stock_rsi_df_T = stock_rsi_df_T.rename(columns={ 0: 'RSI'})
#create a unique date column
stock_rsi_df_T = stock_rsi_df_T.reset_index()
stock_rsi_df_T = stock_rsi_df_T.rename(columns={ 'index': 'date'})
stock_rsi_df_T[['1','2']] = stock_rsi_df_T['date'].str.split('.',expand=True)
stock_rsi_df_T = stock_rsi_df_T.drop(['date', '2'], axis = 1)
stock_rsi_df_T = stock_rsi_df_T.rename(columns={ '1': 'date'})

#save to excel
excel_name_rsi = symbol+'_RSI.xlsx'
excel_name_price = symbol+'_Price.xlsx
stock_rsi_df_T.to_excel(excel_name_rsi, sheet_name='RSI')
stock_price_df.to_excel(excel_name_price, sheet_name='Price_History')
