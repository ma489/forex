import time

from fx.exchangesim.trader.generators.OrderGenerator import OrderGenerator
from fx.historicvis.data.RetrieveData import RetrieveData

GAP_SECONDS = 3
RD = RetrieveData()

# simulate trades; at some point there will be interactive UI
class TraderSimulator(object):
    def __init__(self):
        #print("Retrieving...")
        # result = RD.retrieve_all("GBPUSD")
        #print("Retrieved.")
        # TODO get agg values from DB - not working? model as normal distribution?
        minAsk = 1.502720
        maxAsk = 1.549780
        minBid = 1.502690
        maxBid = 1.549710
        self.o = OrderGenerator(minAsk, maxAsk, minBid, maxBid)

    def start(self, q):
        orderid = 0
        while True:
            order = self.o.generateOrder(orderid)
            #print(order)
            q.put(order)
            time.sleep(GAP_SECONDS)
            orderid += 1
