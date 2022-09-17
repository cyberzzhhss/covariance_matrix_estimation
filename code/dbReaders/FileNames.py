# add relatvie path
import sys
sys.path.append('../')
import os
import os.path

import glob
from collections import deque

class FileNames(object):

    # get parrent dicrectory of the current working directory
    TAQPath = os.path.dirname(os.getcwd())
    BinRTTradesDir = "trades/"
    BinRQQuotesDir = "quotes/"

    @staticmethod
    def getListOfBinRTFiles( dateDir ):
        # dateDir is the full path name of a particular sub-directory
        # containing *.binRT files - one per ticker - for one day of
        # data, e.g. "/Users/lee/TAQ/trades/20070620"
        return deque( glob.glob( "%s/*_trades.binRT" % dateDir ) )
    
    @staticmethod
    def getListOfBinRTDates( binRTTradesDir ):
        return deque( glob.glob( "%s/2007*" % binRTTradesDir ) )
    
    @staticmethod
    def getMergedDayOfTradesFile( dateDir ):
        # dateDir is the full path name of a particular sub-directory
        # containing one gzipped binary file with all trades for all
        # tickers for that day, e.g. BaseGZDir + "/trades/20070620/f1.gz9"
        return ( FileNames.getListOfGZTradeFiles( dateDir ) )[ 0 ]
    
    @staticmethod
    def getListOfGZTradeFiles( dateDir ):
        # dateDir is the full path name of a particular sub-directory
        # containing one gzipped binary file with all trades for all
        # tickers for that day, e.g. BaseGZDir + "/trades/20070620/f1.gz9"
        return deque( glob.glob( "%s/*.gz*" % dateDir ) )
    
    @staticmethod
    def getListOfGZTradeDates():
        return deque( glob.glob( "%s/2007*" % FileNames.GZTradesDir ) )
        
        