import unittest

from dbReaders.FileNames import FileNames
from impactModel.FirstPriceBuckets import FirstPriceBuckets
from dbReaders.TAQTradesReader import TAQTradesReader
import os
from RiskAnalysis import RiskAnalysis
import numpy as np

class Test_RiskAnalysis(unittest.TestCase):

    def testConstructor(self):
        analysis_test = RiskAnalysis(
            T_total=5070, T=650, T_out=39, inputRets='returns.txt')
        fake_data = np.array([[2, 1, 7], [3, 2, 9]])
        expected = np.array([[-0.54178226, -1.52879589,  0.47114814],
                        [-0.58737343, -1.51537793,  0.48293385]])
        res = analysis_test.standardize_returns(fake_data)

        np.random.seed(2022)
        X = np.random.uniform(-1, 1, (2, 3))
        t = 0
        T_out = 2
        w = np.ones(2)
        test_case = ((w[0] * X[0, 1] + w[1] * X[1, 1]) ** 2
                    + (w[0] * X[0, 2] + w[1] * X[1, 2]) ** 2) / T_out
        res2 = analysis_test.oos_var(t, T_out, w, X)
        
        self.assertTrue(res2 == test_case)
        self.assertTrue(np.sum(res - expected) < 0.00000001)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName
    # ']
    unittest.main()
