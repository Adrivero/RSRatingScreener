import pandas as pd
import requests

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
        print(df)
    else:
        df = pd.concat([getNyseStocks(), getNasdaqStocks()], ignore_index=False)
        df.rename(columns={"s":"Ticker"}, inplace=True)

    return df

#TODO make a function that treats the data frame eliminatign null values on revenue and in other columns?
