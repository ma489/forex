from queue import Queue
from threading import Thread
import asyncio
import websockets
from fx.exchangesim.exchange.OrderMatcher import OrderMatcher
from fx.exchangesim.trader.TraderSimulator import TraderSimulator

q = Queue()  # set size?
output = Queue()


def producer():
    ts = TraderSimulator()
    ts.start(q)


def consumer():
    order_matcher = OrderMatcher(output)
    order_matcher.start(q)


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
