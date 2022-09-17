from numpy import floor


class FirstPriceBuckets(object):
    '''
    This class makes price buckets using the first price.
    '''

    def __init__(
            self,
            data,  # Must implement getPrice(i), getTimestamp(i), and getN()
            numBuckets,
            startTS,  # eg 930AM = 19 * 60 * 60 * 1000 / 2
            endTS  # eg. 4PM = 16 * 60 * 60 * 10000
    ):
        '''
        All of the work of making buckets is performed here. The rest
        of the class provides access to the results.
        '''
        # Make sure data is in the right format
        if (data is None) or (data.getPrice is None) or (data.getTimestamp is None) or (data.getN is None):
            raise Exception("Your data object must implement getPrice(i), getTimestamp(i), and getN() methods")

            # Save start and end times
        if startTS is None:
            startTS = 19 * 60 * 60 * 1000 / 2
        if endTS is None:
            endTS = 16 * 60 * 60 * 1000
        self._startTS = startTS
        self._endTS = endTS
        bucketLen = (endTS - startTS) / numBuckets

        # Initialize timestamp and price lists
        self._timestamps = [None] * numBuckets
        self._prices = [None] * numBuckets

        iBucket = -1  # The 0th bucket
        nRecs = data.getN()
        for startI in range(0, nRecs):
            timestamp = data.getTimestamp(startI)
            # Are we past the end of good data?
            if timestamp >= endTS:
                # Yes, we are past the end of good data
                # Stop computing data buckets
                break
            # No we are not pas the end of good data
            # Are we still iterating over data that appears before
            #   the specified start of good data?
            if timestamp < startTS:
                # Yes, we have to skip this data
                continue
            newBucket = int(floor((timestamp - startTS) / bucketLen))
            if iBucket != newBucket:
                # This is a new bucket

                # Append the first value of the new bucket
                self._timestamps[newBucket] = timestamp
                self._prices[newBucket] = data.getPrice(startI)

                # Save our new bucket count
                iBucket = newBucket

    def getPrice(self, index):
        return self._prices[index]

    def getTimestamp(self, index):
        return self._timestamps[index]

    def getN(self):
        return len(self._prices)

    # Exclude buckets with big gaps
