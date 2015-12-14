from queue import Queue
from threading import Thread
import asyncio
import datetime
import websockets
from fx.sim.exchange.OrderDao import OrderDao
from fx.sim.exchange.OrderMatcher import OrderMatcher
from fx.sim.trader.TraderSimulator import TraderSimulator

q = Queue()  # TODO set size
output = Queue()


def producer():
    ts = TraderSimulator()
    ts.start(q)


def consumer():
    order_dao = OrderDao()
    order_matcher = OrderMatcher(order_dao, q)
    while True:
        order = q.get()
        order_id = abs(hash(order))  # TODO is this unique?
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print(now + " > Received order #%d" % order_id)
        output.put(str(order) + " - #%d" % order_id)
        # TODO update UI with new order
        matched_order = order_matcher.match(order)  # match against queue and database
        if matched_order is not None:
            matched_order_id = abs(hash(matched_order))
            output.put("Matched order #%d with #%d" % (order_id, matched_order_id))
            # TODO update UI (bid, ask, last)
            # TODO update queue
        else:
            print("!Failed to match order #%d" % order_id)
            q.put(order)
            order_dao.persist(order)  # TODO if not, persist to mongo DB with other yet-unmatched orders
            # only keep highest precendence orders in queue?
            # q.join?


@asyncio.coroutine
def main(websocket, path):
    prod = Thread(target=producer)
    prod.start()
    cons = Thread(target=consumer)
    cons.start()
    while True:
        message = output.get()
        yield from websocket.send(message)


start_server = websockets.serve(main, '127.0.0.1', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
