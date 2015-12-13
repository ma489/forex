# TODO stable marriage
# TODO try to match order with existing orders (stable-marriage algorithm, with time and price predecence/preference)

class OrderMatcher(object):
    def __init__(self, order_dao):
        self.order_dao = order_dao

    def match(self, order):
        pass
