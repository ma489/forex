import time
from fx.historicvis.web.RetrieveData import RetrieveData
from fx.sim.trader.generators.OrderGenerator import OrderGenerator
from queue import Queue

GAP_SECONDS = 3
RD = RetrieveData()


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
        while True:
            # simulate trades; at some point there will be interactive UI
            order = self.o.generateOrder()
            #print(order)
            q.put(order)
            time.sleep(GAP_SECONDS)
            # TODO add to message queue?
