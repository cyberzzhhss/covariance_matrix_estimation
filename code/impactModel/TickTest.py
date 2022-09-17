class TickTest(object):
    '''
    This class implements the tick test for inferring the direction
    of trades.
    '''
    TOLERANCE = 0.00001

    def __init__(self):
        self.side = 0
        self.prevPrice = 0

    def classify(self, newPrice):
        if self.prevPrice != 0:
            if newPrice > (self.prevPrice + type(self).TOLERANCE):
                self.side = 1
            else:
                if newPrice < (self.prevPrice - type(self).TOLERANCE):
                    self.side = -1
        self.prevPrice = newPrice
        return self.side

    def classifyAll(self, data, startTimestamp, endTimestamp):
        classifications = [0] * data.getN()  # That's the most space we might need
        startI = 0
        for i in range(0, data.getN()):
            if data.getTimestamp(i) < startTimestamp:
                continue
            if data.getTimestamp(i) >= endTimestamp:
                break
            classifications[startI] = (data.getTimestamp(i), data.getPrice(i), self.classify(data.getPrice(i)))
            startI = startI + 1
        return classifications[0:startI]
