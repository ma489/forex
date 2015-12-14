# TODO stable marriage
# TODO try to match order with existing orders (stable-marriage algorithm, with time and price predecence/preference)
from fx.sim.model.Order import Order


class OrderMatcher(object):
    def __init__(self, order_dao, q):
        self.q = q
        self.order_dao = order_dao

    def match(self, order):
        return Order(None, None, None, None)
