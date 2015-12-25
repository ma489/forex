from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType


# NYSE rules
def price(order, matched_order, best_bid, best_ask, reference_price):
    if order.order_conditions is OrderConditions.Market and matched_order.order_conditions is OrderConditions.Market:
        return price_two_market_orders(best_ask, best_bid, matched_order, reference_price)
    elif order.order_conditions is OrderConditions.Limit and matched_order.order_conditions is OrderConditions.Market:
        return order.order_price
    elif order.order_conditions is OrderConditions.Market and matched_order.order_conditions is OrderConditions.Limit:
        return matched_order.order_price
    elif order.order_conditions is OrderConditions.Limit and matched_order.order_conditions is OrderConditions.Limit:
        # Prefer the price of the resting order (it came first) - "Discriminatory pricing rule"
        return matched_order.order_price


def price_two_market_orders(best_ask, best_bid, matched_order, reference_price):
    if matched_order.order_type is OrderType.Buy:
        if best_bid == -1.0:
            return reference_price
        else:
            return best_bid
    else:  # i.e. sell
        if best_ask == -1.0:
            return reference_price
        else:
            return best_ask
