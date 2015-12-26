import sys
sys.path.append('/home/mansour/dev/trading-sim')
print(sys.path)

from queue import Queue
from threading import Thread
from fx.exchangesim.exchange.OrderMatcher import OrderMatcher
from fx.exchangesim.trader.TraderSimulator import TraderSimulator
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

POISON_PILL = "@POISON_PILL@"


class Exchange:
    def __init__(self, ws):
        self.q = Queue()  # set size?
        self.output = Queue()
        self.ws = ws
        self.simulator = TraderSimulator()

    def producer(self):
        self.simulator.start(self.q)

    def consumer(self):
        order_matcher = OrderMatcher(self.output)
        order_matcher.start(self.q)

    def output_writer(self):
        print("running output_writer")
        while True:
            message = self.output.get()
            if message == POISON_PILL:
                break
            msg_string = message.encode('utf8')
            self.ws.sendMessage(msg_string)

    def start_exchange(self):
        prod = Thread(target=self.producer)
        prod.start()
        cons = Thread(target=self.consumer)
        cons.start()
        output_thread = Thread(target=self.output_writer)
        output_thread.start()

    def kill(self):
        print("Dying...")
        self.output.put(POISON_PILL)
        self.q.put(POISON_PILL)
        self.simulator.kill()
        print("Dead.")


class ServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.exchange = Exchange(self)

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.exchange.start_exchange()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.exchange.kill()


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8081", debug=False)
    factory.protocol = ServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 8081)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
