import unittest

from dbReaders.FileNames import FileNames
from impactModel.FirstPriceBuckets import FirstPriceBuckets
from dbReaders.TAQTradesReader import TAQTradesReader
import os
from PrepareReturnsMatrix import process_data


class Test_PreareReturnsMatrix(unittest.TestCase):

    def testConstructor(self):
        returns = process_data(0, 1)
        self.assertTrue(returns[0][1] == 0.0005089175102275245)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName
    # ']
    unittest.main()