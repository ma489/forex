import random

#Generates random prices in ranges minAsk-maxAsk, and minBid-maxBid
# current market price?
class PriceGenerator(object):
    def __init__(self, minask, maxask, minbid, maxbid):
        self.minAsk = minask
        self.maxAsk = maxask
        self.minBid = minbid
        self.maxBid = maxbid

    def generateAskPrice(self):
        return random.uniform(self.minAsk, self.maxAsk) #TODO 4dp?

    def generateBidPrice(self):
        return random.uniform(self.minBid, self.maxBid) #TODO 4dp?
