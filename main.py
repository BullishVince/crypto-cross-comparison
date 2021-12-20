import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sys

def read_top100_from_file(number_of_currencies):
    with open("top100.txt", "r") as f:
        list = [line.rstrip() for line in f]
        return list[:number_of_currencies]

def get_top100_cryptocurrencies(): #I manually call this function once in a while to update my local file containing top 100 cryptos
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = json.loads(requests.get(url).text)
    f = open("top100.txt", "w")
    for currency in data:
        if 'usd' not in currency['symbol']:
            f.write(currency['symbol'] + '\n')
    print("Saved Top 100 cryptocurrencies to file top100.txt")
    f.close()

def get_bars(symbol, interval = '30m'):
   root_url = 'https://api.binance.com/api/v1/klines'
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df

def plot_pair(pair):
    initialPrice = float(pair[1].loc[startingDate].first('1D')['c'].astype('float')/basePair.loc[startingDate].first('1D')['c'].astype('float'))
    percentage = ((pair[1]['c'].astype('float')/basePair['c'].astype('float'))/initialPrice)*100
    percentage.plot(figsize=(12,7), label=pair[0])


#####Main code starts here#####
print("Running script for " + sys.argv[1] + " [" + sys.argv[2] + " -> Now] ...")
startingDate = sys.argv[2]
basePair = get_bars(sys.argv[1]).loc[startingDate:]

# get_top100_cryptocurrencies() #Run this line if you want to fetch the current top 100 cryptos and save them to file top100.txt

currencyList = read_top100_from_file(5)
pairList = list()
for currencySymbol in currencyList:
    ticker = currencySymbol.upper() + 'USDT'
    print('Fetching historical prices for [' + ticker + ']')
    pairList.append([ticker, get_bars(ticker).loc[startingDate:]])

for pair in pairList:
    plot_pair(pair)
plt.hlines(y=100, xmin=min(pairList[0][1].index), xmax=max(pairList[0][1].index), colors='black', linestyles='-', lw=2)
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5, axis = 'y')
plt.legend(loc='upper left')
plt.show()
