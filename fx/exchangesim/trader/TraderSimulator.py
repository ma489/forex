import time

from fx.exchangesim.trader.generators.OrderGenerator import OrderGenerator
from fx.historicvis.data.RetrieveData import RetrieveData

GAP_SECONDS = 5
RD = RetrieveData()

# simulate trades; at some point there will be interactive UI
class TraderSimulator(object):
    def __init__(self):
        #print("Retrieving...")
        # result = RD.retrieve_all("GBPUSD")
        #print("Retrieved.")
        # TODO get agg values from DB - not working? model as normal distribution?
        minAsk = 1.5027
        maxAsk = 1.5498
        minBid = 1.5027
        maxBid = 1.5497
        self.o = OrderGenerator(minAsk, maxAsk, minBid, maxBid)

    def start(self, q):
        orderid = 0
        while True:
            order = self.o.generateOrder(orderid)
            q.put(order)
            time.sleep(GAP_SECONDS)
            orderid += 1
