from impactModel import FileManager

from impactModel.FirstPriceBuckets import FirstPriceBuckets
from impactModel.LastPriceBuckets import LastPriceBuckets
from impactModel.TickTest import TickTest
from impactModel.VWAP import VWAP

from dbReaders import FileNames
from dbReaders.TAQTradesReader import TAQTradesReader
from dbReaders.TAQQuotesReader import TAQQuotesReader

from ReturnBuckets import ReturnBuckets

import os
import numpy as np

def process_data(start=0, end=65):
    with open('validDays.txt') as f1:
        validDays = [line.rstrip('\n') for line in f1]
    with open('validTickers.txt') as f2:
        validTickers = [line.rstrip('\n') for line in f2]

    numOfDays = len(validDays)
    numOfTickers = len(validTickers)
    numOfTimes = numOfDays*78

    #LOOP THRU TICKER AND DATA
    tickerIndex = 0  # ticker
    dayIndex = 0  # date


    startTS930 = 19*60*60*1000/2
    endTS1530 = 31*60*60*1000/2
    endTS1600 = 16*60*60*1000

    returns = np.ones((numOfTickers, numOfTimes))*0.000000001
    baseDir = os.path.dirname(os.getcwd())

    for dayIndex in range(start, end):
        padding = dayIndex*78
        for tickerIndex in range(numOfTickers):
            #ex. "trades/20070620/IBM_trades.binRT"
            fileName = "trades/" + \
                str(validDays[dayIndex])+"/" + \
                validTickers[tickerIndex]+"_trades.binRT"
            #print(fileName)
            data = TAQTradesReader(baseDir + "/" + fileName)
            returnBuckets = ReturnBuckets(data, startTS930, endTS1600, 78)
            for binIndex in range(77):
                tempReturn = returnBuckets.getReturn(binIndex)
                if tempReturn != None:
                    returns[tickerIndex][binIndex+padding] = tempReturn
                tempReturn = 0
        print("done with "+str(validDays[dayIndex]))
        if dayIndex % 10 == 0:
            np.savetxt('test_returns.txt', returns)
    np.savetxt('test_returns.txt', returns)

    return returns

if __name__ == "__main__":
    process_data()