import time

from fx.exchangesim.trader.OrderGenerator import OrderGenerator
from fx.historicvis.data.RetrieveData import RetrieveData

GAP_SECONDS = 5
RD = RetrieveData()

# Makes sure bid<ask invariant is maintained
minAsk = 1.5263
maxAsk = 1.5498
minBid = 1.5027
maxBid = 1.5262


# Simulate orders
class TraderSimulator(object):
    def __init__(self):
        self.o = OrderGenerator(minAsk, maxAsk, minBid, maxBid)


    #TODO make sure the market is pretty liquid (balance of buy and sell)
    def start(self, q):
        orderid = 0
        while True:
            order = self.o.generateOrder(orderid)
            q.put(order)
            time.sleep(GAP_SECONDS)
            orderid += 1
