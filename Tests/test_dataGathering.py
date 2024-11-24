import unittest
import pandas as pd
from RSRatingScreener.Source.Functions.dataGathering import *

class TestNasdaqAndSPX(unittest.TestCase):
    def test_numberStocks(self):
        df = get_US_Stocks()
        numberOfStocks = len(df)
        #I choose 5200 as an arbitrary value. Stocks may be delisted from exchanges.
        self.assertGreater(numberOfStocks,5200, "Wrong number of stocks added, the 24/11/2024 I had 5263, "
         "meaning we've lost some stocks during the GET request or concatenation of dataframes")
