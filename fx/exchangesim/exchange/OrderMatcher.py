from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType


class OrderMatcher(object):
    def __init__(self, buy_orders, sell_orders):
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

    # TODO what is this algorithm? pseudo-stable-marriage-bin-packing?
    def match(self, order):
        if order.order_type is OrderType.Buy:
            candidates = self.sell_orders
            candidates.sort(key=lambda o: (o.order_price, o.entry_time)) #sort by ascending price, then entry time
        else:
            candidates = self.buy_orders
            candidates.sort(key=lambda o: (-o.order_price, o.entry_time)) #sort by descending price, then entry time
        for candidate in candidates:
            if candidate == order:
                continue
            if price_is_right(candidate, order):
                return candidate
        else:
            return None


def price_is_right(candidate, order):
    if order.order_conditions is OrderConditions.Market:
        return True
    elif order.order_conditions is OrderConditions.Limit:
        if order.order_type is OrderType.Buy:
            if candidate.order_price <= order.order_price:
                return True
        else:
            if candidate.order_price >= order.order_price:
                return True
    return False
