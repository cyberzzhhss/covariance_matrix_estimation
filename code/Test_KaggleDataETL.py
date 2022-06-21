import unittest

from dbReaders.FileNames import FileNames
from impactModel.FirstPriceBuckets import FirstPriceBuckets
from dbReaders.TAQTradesReader import TAQTradesReader
import os
from KaggleDataETL import process_kaggle_data

class Test_KaggleDataETL(unittest.TestCase):

    def testConstructor(self):
        returns = process_kaggle_data(src='all_stocks_5yr.csv')
        self.assertTrue(returns[0][0] == -0.019661016949152486)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName
    # ']
    unittest.main()