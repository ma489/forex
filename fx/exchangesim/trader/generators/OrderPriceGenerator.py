import random
# Generates random prices in ranges minAsk-maxAsk, and minBid-maxBid
# TODO incorporate current market price?
from math import trunc


class PriceGenerator(object):
    def __init__(self, minask, maxask, minbid, maxbid):
        self.minAsk = minask
        self.maxAsk = maxask
        self.minBid = minbid
        self.maxBid = maxbid

    def generateAskPrice(self):
        x = random.uniform(self.minAsk, self.maxAsk)
        return self.truncate_to_4dp(x)

    def generateBidPrice(self):
        x = random.uniform(self.minBid, self.maxBid)
        return self.truncate_to_4dp(x)

    def truncate_to_4dp(self, x):
        return float(trunc(x * 10000)) / 10000
