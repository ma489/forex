import time

from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType
from fx.exchangesim.exchange.TradePricer import price

buyOrders = []
sellOrders = []
closePrice = 1.5262  # previous day
last = closePrice
referencePrice = closePrice


class OrderMatcher(object):
    def __init__(self, output_queue):
        self.output = output_queue

    # TODO what is this algorithm? pseudo-stable-marriage-bin-packing?
    # Precedence: Market over limit, then price precedence, then time precedence
    def match(self, order):
        if order.order_type is OrderType.Buy:
            candidates = sellOrders
            # sort by: market over limit, then ascending price, then entry time
            sort_sell_orders(candidates)
        else:
            candidates = buyOrders
            # sort by: market over limit, then descending price, then entry time
            sort_buy_orders(candidates)
        for candidate in candidates:
            if candidate == order:
                continue
            if price_is_right(candidate, order):
                return candidate
        else:
            return None

    # TODO use objects not strings to communicate with front end?
    def handle_matched_order(self, matched_order, order):
        original_order_remaining_unfilled = order.remaining_unfilled
        original_matched_order_remaining_unfilled = matched_order.remaining_unfilled
        order.remaining_unfilled -= original_matched_order_remaining_unfilled
        matched_order.remaining_unfilled -= original_order_remaining_unfilled
        if order.remaining_unfilled <= 0:
            order.remaining_unfilled = 0
            remove_order(order)
            self.output.put("Filled %s %d" % (order.order_id, order.order_size))
        else:
            self.output.put("Partial: %s,Original: %d,Current: %d"
                            % (order.order_id, order.order_size, order.order_size - order.remaining_unfilled))
        if matched_order.remaining_unfilled <= 0:
            matched_order.remaining_unfilled = 0
            remove_order(matched_order)
            self.output.put("Filled %s %d" % (matched_order.order_id, matched_order.order_size))
        else:
            self.output.put("Partial: %s,Original: %d,Current: %d"
                            % (matched_order.order_id, matched_order.order_size,
                               matched_order.order_size - matched_order.remaining_unfilled))
        self.settle(matched_order, order, original_matched_order_remaining_unfilled, original_order_remaining_unfilled)

    def settle(self, matched_order, order, original_matched_order_remaining_unfilled,
               original_order_remaining_unfilled):
        print("Matched order #%s (%d before, %d after) with #%s (%d before, %d after)"
              % (order.order_id, original_order_remaining_unfilled, order.remaining_unfilled, matched_order.order_id,
                 original_matched_order_remaining_unfilled, matched_order.remaining_unfilled))
        order_size = original_order_remaining_unfilled - order.remaining_unfilled
        global last
        global referencePrice
        last = price(order, matched_order, get_bid(), get_ask(), referencePrice)
        self.output.put("Matched #%s with #%s - %d @ %.4f" % (order.order_id, matched_order.order_id, order_size, last))
        referencePrice = last
        self.update_prices()

    def update_prices(self):
        # TODO check for possible violation of bid<ask when using reference price
        bid = get_bid()
        ask = get_ask()
        last_direction = get_direction()
        spread = (ask - bid) * 10000  # pips
        self.output.put("PriceUpdate#Bid: %.4f,Ask: %.4f,Last: %.4f %d,Spread: %d" % (bid, ask, last, last_direction, spread))

    def start(self, q):
        while True:
            order = q.get()
            if order.remaining_unfilled <= 0:
                continue
            already_exists = add_to_order_book(order)
            if not already_exists:
                self.update_prices()
                self.output.put(str(order))
            matched_order = self.match(order)
            while matched_order is not None and order.remaining_unfilled > 0:
                self.handle_matched_order(matched_order, order)
                time.sleep(1)
                matched_order = self.match(order)
                # at some point, handle FOK or AON orders


# ignorable fp comparison
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


# precedence: type, price and entry time
def add_to_order_book(order):
    if order.order_type is OrderType.Buy:
        if order not in buyOrders:
            buyOrders.append(order)
            return False
        else:
            return True
    else:  # i.e. sell order
        if order not in sellOrders:
            sellOrders.append(order)
            return False
        else:
            return True


def remove_order(order):
    if order.order_type is OrderType.Buy:
        buyOrders.remove(order)
    else:
        sellOrders.remove(order)


def get_bid():
    if len(buyOrders) == 0:
        return referencePrice
    sort_buy_orders(buyOrders)
    for buyOrder in buyOrders:
        if buyOrder.order_price > -1.0:  # ignorable fp comparison
            return buyOrder.order_price
    price = buyOrders[0].order_price
    if price == -1.0:  # ignorable fp comparison
        return referencePrice
    return price


def get_ask():
    if len(sellOrders) == 0:
        return referencePrice
    sort_sell_orders(sellOrders)
    for sellOrder in sellOrders:
        if sellOrder.order_price > -1.0:
            return sellOrder.order_price
    price = sellOrders[0].order_price
    if price == -1.0:
        return referencePrice
    return price


def get_direction():
    if closePrice < last:
        return 1
    elif closePrice > last:
        return -1
    else:
        return 0
