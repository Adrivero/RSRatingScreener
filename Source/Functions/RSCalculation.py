#STOCK PRRICES ARE NOT SPLIT ADJUSTED. THIS MAY GIVE INCORRECT VALUES OF RELATIVE STRENGTH
from RSRatingScreener.Source.Functions.dataGathering import *

#TODO hacer que funcione para acciones como BRK.A (sustituirlas por simplemente BRK?)

def calculate_RS_stock(ticker):
    P3=getStockPerformance(ticker,"3mo")
    P6=getStockPerformance(ticker,"6mo")
    P9 = getStockPerformance(ticker, "9mo")
    P12 = getStockPerformance(ticker, "1y")

    rs = 0.4*P3 + 0.2*P6 + 0.2*P9 + 0.2*P12

    return rs

def calculate_RS_sp500():
    ticker = "^GSPC"
    P3 = getStockPerformance(ticker, "3mo")
    P6 = getStockPerformance(ticker, "6mo")
    P9 = getStockPerformance(ticker, "9mo")
    P12 = getStockPerformance(ticker, "1y")

    rs = 0.4 * P3 + 0.2 * P6 + 0.2 * P9 + 0.2 * P12

    return rs

def calculate_RS_score(ticker):
    tickerList = getTickersOfAllStocks()
    all_rs=[]

    #TODO We need to check if yfinance and our web can correctly retrieve the ticker. Some special tickers such as
    #TODO BRK.A for class A are not available

    #TODO we can't calculate IPOS performance for 6 months

    for x in tickerList:
       score = (1+calculate_RS_stock(x))/(1+calculate_RS_sp500())
       all_rs.append(score)

    print("Lista de tickers" + tickerList)

    sortedRs = all_rs.sort()
    print("lista de sorted RS:" + sortedRs)

calculate_RS_score("TSLA")




