import random

from fx.sim.model.OrderType import OrderType


class OrderTypeGenerator(object):
    def __init__(self):
        self.data = []

    def generateOrderType(self):
        return random.choice(list(OrderType))
