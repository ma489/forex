from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType


class OrderMatcher(object):
    def __init__(self, buy_orders, sell_orders):
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

    # TODO what is this algorithm? pseudo-stable-marriage-bin-packing?
    # Precedence: Market over limit, then price precedence, then time precedence
    def match(self, order):
        if order.order_type is OrderType.Buy:
            candidates = self.sell_orders
            # sort by: market over limit, then ascending price, then entry time
            sort_sell_orders(candidates)
        else:
            candidates = self.buy_orders
            # sort by: market over limit, then descending price, then entry time
            sort_buy_orders(candidates)
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


def sort_sell_orders(candidates):
    candidates.sort(key=lambda o: (o.order_conditions.value, o.order_price, o.entry_time))


def sort_buy_orders(candidates):
    candidates.sort(key=lambda o: (o.order_conditions.value, -o.order_price, o.entry_time))
