class VWAP(object):
    '''
    This class calculates the volume weighted average price between
    a start time and an end time (exclusive).
    '''

    def __init__(self, data, startTS, endTS):
        '''
        This does all the processing and gives the client access to the
        results via getter methods.
        '''

        # Make sure data is in the right format
        if (data is None) or (data.getPrice is None) or (data.getTimestamp is None) or (data.getPrice is None) or (
                data.getN is None):
            raise Exception("Your data object must implement getTimestamp(i), getSize(i), getPrice(i), and getN() "
                            "methods")

        v = 0
        s = 0
        counter = 0
        for i in range(0, data.getN()):
            if data.getTimestamp(i) < startTS:
                continue
            if data.getTimestamp(i) >= endTS:
                break
            counter = counter + 1
            v = v + (data.getSize(i) * data.getPrice(i))
            s = s + data.getSize(i)
        if counter == 0:
            self.counter = 0
            self.vwap = None
        else:
            self._counter = counter
            self._vwap = v / s

    def getVWAP(self):
        return self._vwap

    def getN(self):
        return self._counter
