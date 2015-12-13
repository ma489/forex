import random

#Generates random but realistic order sizes
#Historically, one trade size: 100,000 units of currency
#Technology has changed this
#Micro Lot = 1,000 unit trade
#Mini Lot = 10,000 unit trade
#Standard Lot = 100,000 unit trade
#Yard = 1 billion units
#e.g. 1 Micro lot GBPUSD = £1000. 1 Standard Lot GBPUSD = £1,000,000

MIN_ORDER_SIZE = 1000
MAX_ORDER_SIZE = 1000000

class OrderSizeGenerator(object):
    def __init__(self):
        self.data = []

    def generateOrderSize(self):
        return random.randrange(MIN_ORDER_SIZE, MAX_ORDER_SIZE, MIN_ORDER_SIZE)
