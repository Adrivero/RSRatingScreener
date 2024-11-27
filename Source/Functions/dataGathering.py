import pandas as pd
import requests
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

#Returns data frame with information about all Nasdaq Stocks
#It is necessary to change maxTableNumber according to the number of pages the thable has when you visit:
#https://stockanalysis.com/list/nasdaq-stocks/ in order to retrieve the data correctly.
def getNasdaqStocks(url = "https://api.stockanalysis.com/api/screener/s/f",maxTableNumber=7):
    responseJson=[]
    stocklist = pd.DataFrame()
    for i in range(1,maxTableNumber+1):
        params = {
            "m": "marketCap",
            "s": "desc",
            "c": "no,s,n,marketCap,price,change,revenue",
            "cn": 500,
            "f": "exchange-is-NASDAQ",
            "p": i,
            "i": "stocks"
        }

        rsp=requests.get(url, params=params)

        if rsp.status_code == 200:
            responseTransformed=rsp.json()
            responseTransformed.pop("status")

            responseJson.append(responseTransformed)
            df = pd.json_normalize(responseJson[i-1]['data']['data'])

            stocklist = pd.concat([stocklist,df],ignore_index=True)
        else: print(f"Error on Nasdaq Stocks request. Request with parameter- p:{i}")
        stocklist["Exchange"]="Nasdaq"
    return stocklist

#Returns data frame with information about all SPY Stocks
#It is necessary to change maxTableNumber according to the number of pages the thable has when you visit:
#https://stockanalysis.com/list/nyse-stocks/ in order to retrieve the data correctly.
def getNyseStocks(url="https://api.stockanalysis.com/api/screener/s/f",maxTableNumber=4):
    responseJson = []
    stocklist = pd.DataFrame()
    for i in range(1, maxTableNumber+1):
        params = {
            "m": "marketCap",
            "s": "desc",
            "c": "no,s,n,marketCap,price,change,revenue",
            "cn": 500,
            "f": "exchange-is-NYSE",
            "p": i,
            "i": "stocks"
        }
        # print(params)

        rsp = requests.get(url, params=params)

        if rsp.status_code == 200:
            responseTransformed = rsp.json()
            responseTransformed.pop("status")

            responseJson.append(responseTransformed)
            df = pd.json_normalize(responseJson[i - 1]['data']['data'])

            stocklist = pd.concat([stocklist, df], ignore_index=True)
        else:
            print(f"Error on NYSE Stocks request. Request with parameter- p:{i}")
            
        stocklist["Exchange"]="Nyse"
    return stocklist

#Returns data frame with the information of all US stocks (excluding minor exchanges) as a data frame
#If resetIndex parameter is False, it won't reset indexes. [0,1,....,2000,0,1,....3000] (First NYSE then NASDAQ)
def get_raw_US_Stocks(resetIndex=True):
    df = pd.DataFrame()
    if resetIndex:
        df = pd.concat([getNyseStocks(),getNasdaqStocks()],ignore_index=True)
        df.rename(columns={"s":"Ticker"}, inplace=True)
    else:
        df = pd.concat([getNyseStocks(), getNasdaqStocks()], ignore_index=False)
        df.rename(columns={"s":"Ticker"}, inplace=True)

    df.rename(columns={"n":"Name"}, inplace=True)
    df.fillna(0, inplace=True)
    df.drop(columns=["no"],inplace=True)
    return df

#Returns a list with the Ticker of all stocks of the USA
def  getTickersOfAllStocks():
    df = get_raw_US_Stocks()
    df_filtered = df[~df['Ticker'].str.contains('\\.', na=False)]

    return df_filtered["Ticker"].tolist()

#Uses yahoo finance api to get current stock price. Returns float value
def getCurrentPrice(ticker):
    try:
        stock_data = yf.Ticker(ticker)
        currentPrice = stock_data.history(period="1d")["Close"]
        return float(currentPrice.iloc[0])
    except Exception as nonFoundTicker:
        print(f"Error, Ticker: {ticker} not found in yfinance in getCurrentPrice")




#Gets stock performance for a certain period
#period= "3mo" | "6mo" | "9mo" | "1y" |
def getStockPerformance(ticker, time):
    try:
        stock_data = yf.Ticker(ticker)
    except Exception as nonFoundTicker:
        print(f"Error, Ticker: {ticker} not found in yfinance in getStockPerformance")

    #We cannot get the performance for 9 months the same way we get the others as yfinance doesn't support 9mo interval
    if time=="9mo":
        currentDate = datetime.today()
        #To calculate the date 9 months ago we use relative delta:
        nineMoAgoDate=currentDate-relativedelta(months=9)

        #Transform it from datetime to string
        nineMoAgoDate=nineMoAgoDate.strftime('%Y-%m-%d')

        history= stock_data.history(start=nineMoAgoDate, end=currentDate.strftime('%Y-%m-%d'))
        nineMoPrice = history['Close'].iloc[0]
        todayPrice = history['Close'].iloc[-1]
        performance = todayPrice/nineMoPrice

        return float(performance)


    priceInLastPeriod = stock_data.history(time)["Close"]
    #We need to transform it into a float value
    priceInLastPeriod = float(priceInLastPeriod.iloc[0])

    performance = getCurrentPrice(ticker)/priceInLastPeriod

    return float(performance)


