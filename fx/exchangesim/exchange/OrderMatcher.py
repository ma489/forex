# TODO stable marriage
# TODO try to match order with existing orders (stable-marriage algorithm, with time and price predecence/preference)

#TODO write tests
class OrderMatcher(object):
    def __init__(self, order_dao):
        self.order_dao = order_dao

    def match(self, order):
        orders = self.order_dao.retrieveAllOrders()
        for ord in orders:
            if ord.order_size >= order.order_size \
                    and ord.order_type != order.order_type \
                    and ord != order:
                return ord
        else:
            return None
