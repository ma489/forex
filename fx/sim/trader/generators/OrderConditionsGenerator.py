import random

from fx.sim.model.OrderConditions import OrderConditions


class OrderConditionsGenerator(object):
    def __init__(self):
        self.data = []

    def generateOrderConditions(self):
        return random.choice(list(OrderConditions))
