import unittest
import pandas as pd
from RSRatingScreener.Source.Functions.dataGathering import *
import io
import re

class TestNasdaqAndSPX(unittest.TestCase):
    def test_number_of_US_Stocks(self):
        df = get_raw_US_Stocks()
        numberOfStocks = len(df)
        #I choose 5200 as an arbitrary value. Stocks may be delisted from exchanges.
        self.assertGreater(numberOfStocks,5200, "Wrong number of stocks added, the 24/11/2024 I had 5263, "
         "meaning we've lost some stocks during the GET request or concatenation of dataframes")


        #---------------------------Check if all null values have been eliminated correctly----------------------

        buffer = io.StringIO()
        # Gets the response of df.info() as a string:
        df.info(buf=buffer)

        s = buffer.getvalue()

        # regex expression that finds the values behind the "non-null" part
        pattern = r"\s+(\d+)\s+non-null"

        # We find all matches using the regex pattern. We need to check if we get a smaller than 7 list (7 is the number of expected
        # columns of the DataFrame Ticker,...,Revenue,Exchange
        matches = re.findall(pattern, s)

        values = [int(match) for match in matches]
        # Transforms the list into a set which doesn't have duplicates
        x = set(values)
        y = True
        # If the set has more than 1 item, it means the given values list has a different element on it
        if len(x) != 1:
            y = False

        msg2=(f"Error when cleaning data, non-zero values haven't been cleaned correctly. One column has less than {len(df)} "
             f"values, so some null value is still in the table. You should check the gathering process or the treatment of the DataFrame"
              f"inside the get_raw_US_Stocks()")
        self.assertTrue(y,msg2)


