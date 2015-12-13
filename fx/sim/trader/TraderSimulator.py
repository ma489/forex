import time

from fx.historicvis.web.RetrieveData import RetrieveData
from fx.sim.trader.generators.OrderGenerator import OrderGenerator

GAP_SECONDS = 3

RD = RetrieveData()
print("Retrieving...")
#result = RD.retrieve_all("GBPUSD")
# TODO get agg values from DB - not working? model as normal distribution?
minAsk = 1.502720
maxAsk = 1.549780
minBid = 1.502690
maxBid = 1.549710
print("Retrieved.")
o = OrderGenerator(minAsk, maxAsk, minBid, maxBid)

while True:
    order = o.generateOrder(minAsk, maxAsk, minBid, maxBid)
    print(order)
    time.sleep(GAP_SECONDS)
    #TODO add to message queue?