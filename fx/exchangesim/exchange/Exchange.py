from queue import Queue
from threading import Thread
import asyncio
import websockets
import time
from fx.exchangesim.exchange.OrderMatcher import OrderMatcher
from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType
from fx.exchangesim.trader.TraderSimulator import TraderSimulator
from fx.exchangesim.exchange.OrderMatcher import sort_buy_orders
from fx.exchangesim.exchange.OrderMatcher import sort_sell_orders

q = Queue()  # TODO set size?
output = Queue()
buyOrders = []
sellOrders = []
closePrice = 1.5262  # previous day
last = closePrice
referencePrice = closePrice


def producer():
    ts = TraderSimulator()
    ts.start(q)


def consumer():
    order_matcher = OrderMatcher(buyOrders, sellOrders)
    while True:
        order = q.get()
        if order.remaining_unfilled <= 0:
            continue
        already_exists = add_to_order_book(order)
        if not already_exists:
            update_prices()
            output.put(str(order))
        matched_order = order_matcher.match(order)
        while matched_order is not None and order.remaining_unfilled > 0:
            handle_matched_order(matched_order, order)
            time.sleep(1)
            matched_order = order_matcher.match(order)
            # else:
            #    handle_unmatched_order(order) only needed for FOK, AON


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


# TODO use objects not strings to communicate with front end?
def handle_matched_order(matched_order, order):
    original_order_remaining_unfilled = order.remaining_unfilled
    original_matched_order_remaining_unfilled = matched_order.remaining_unfilled
    order.remaining_unfilled -= original_matched_order_remaining_unfilled
    matched_order.remaining_unfilled -= original_order_remaining_unfilled
    if order.remaining_unfilled <= 0:
        order.remaining_unfilled = 0
        remove_order(order)
        output.put("Filled %s %d" % (order.order_id, order.order_size))
    else:
        output.put("Partial: %s,Original: %d,Current: %d"
                   % (order.order_id, order.order_size, order.order_size - order.remaining_unfilled))
    if matched_order.remaining_unfilled <= 0:
        matched_order.remaining_unfilled = 0
        remove_order(matched_order)
        output.put("Filled %s %d" % (matched_order.order_id, matched_order.order_size))
    else:
        output.put("Partial: %s,Original: %d,Current: %d"
                   % (matched_order.order_id, matched_order.order_size,
                      matched_order.order_size - matched_order.remaining_unfilled))
    settle(matched_order, order, original_matched_order_remaining_unfilled, original_order_remaining_unfilled)


def settle(matched_order, order, original_matched_order_remaining_unfilled, original_order_remaining_unfilled):
    print("Matched order #%s (%d before, %d after) with #%s (%d before, %d after)"
          % (order.order_id, original_order_remaining_unfilled, order.remaining_unfilled, matched_order.order_id,
             original_matched_order_remaining_unfilled, matched_order.remaining_unfilled))
    global last
    last = price(order, matched_order)
    output.put("Matched order #%s with order #%s" % (order.order_id, matched_order.order_id)) #TODO display last order size & price
    global referencePrice
    referencePrice = last
    update_prices()


def update_prices():
    bid = get_bid()
    ask = get_ask()
    last_direction = get_direction()
    spread = (ask - bid) * 10000 # pips
    output.put("PriceUpdate#Bid: %.4f,Ask: %.4f,Last: %.4f %d,Spread: %d" % (bid, ask, last, last_direction, spread))


def get_direction():
    if closePrice < last:
        return 1
    elif closePrice > last:
        return -1
    else:
        return 0


def get_bid():
    if len(buyOrders) == 0:
        return referencePrice
    sort_buy_orders(buyOrders)
    for buyOrder in buyOrders:
        if buyOrder.order_price > -1.0:
            return buyOrder.order_price
    price = buyOrders[0].order_price
    if price == -1.0:
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


def price(order, matched_order):  # NYSE rules
    if order.order_conditions is OrderConditions.Market and matched_order.order_conditions is OrderConditions.Market:
        if matched_order.order_type is OrderType.Buy:
            best_bid = get_bid()
            if best_bid == -1.0:
                return referencePrice
            else:
                return best_bid
        else:  # i.e. sell
            best_ask = get_ask()
            if best_ask == -1.0:
                return referencePrice
            else:
                return best_ask
    elif order.order_conditions is OrderConditions.Limit and matched_order.order_conditions is OrderConditions.Market:
        return order.order_price
    elif order.order_conditions is OrderConditions.Market and matched_order.order_conditions is OrderConditions.Limit:
        return matched_order.order_price
    elif order.order_conditions is OrderConditions.Limit and matched_order.order_conditions is OrderConditions.Limit:
        return matched_order.order_price  # Prefer the price of the resting order (it came first) - "Discriminatory pricing rule"


def remove_order(order):
    if order.order_type is OrderType.Buy:
        buyOrders.remove(order)
    else:
        sellOrders.remove(order)


@asyncio.coroutine
def main(websocket, path):
    prod = Thread(target=producer)
    prod.start()
    cons = Thread(target=consumer)
    cons.start()
    while True:
        if not websocket.open:
            break
        message = output.get()
        yield from websocket.send(message)


start_server = websockets.serve(main, '127.0.0.1', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
