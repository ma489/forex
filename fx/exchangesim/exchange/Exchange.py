import random
from queue import Queue
from threading import Thread
# import asyncio
# import websockets
from fx.exchangesim.exchange.OrderMatcher import OrderMatcher
from fx.exchangesim.trader.TraderSimulator import TraderSimulator

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

POISON_PILL = "@POISON_PILL@"


class Exchange:

    def __init__(self, ws, id):
        # TODO are these being shared?
        self.q = Queue()  # set size?
        self.output = Queue()
        self.ws = ws
        self.id = id
        self.simulator = TraderSimulator()

    def producer(self):
        # self.simulator = TraderSimulator()
        self.simulator.start(self.q)

    def consumer(self):
        order_matcher = OrderMatcher(self.output)
        order_matcher.start(self.q)

    def output_writer(self):
        print("running output_writer")
        while True:
            # print(ws.state)
            message = self.output.get()
            if message == POISON_PILL:
                print("Got poison pill")
                break
            msg_string = message.encode('utf8')
            print("hi %d", self.id)
            # print(msg_string)
            # prep_msg = PreparedMessage(msg_string, False, applyMask, doNotCompress)
            print("sending on websocket: ")
            print(hash(self.ws))
            self.ws.sendMessage(msg_string)

    def start_exchange(self):
        prod = Thread(target=self.producer)
        prod.start()
        cons = Thread(target=self.consumer)
        cons.start()
        output_thread = Thread(target=self.output_writer)
        output_thread.start()

    def kill(self):
        print("Killing...")
        self.output.put(POISON_PILL)
        self.q.put(POISON_PILL)
        self.simulator.kill()
        # with self.q.mutex:
        #     self.q.queue.clear()
        # with self.output.mutex:
        #     self.output.queue.clear()




# def output_writer():
#     print("running output_writer")
#     while True:
#         # print(ws.state)
#         message = output.get()
#         msgString = message.encode('utf8')
        # print(msgString)
        # ws.sendMessage(msgString, isBinary=False)



# @asyncio.coroutine
# async def main(websocket, path):
#     prod = Thread(target=producer)
#     prod.start()
#     cons = Thread(target=consumer)
#     cons.start()
#     # try:
#     while True:
#         print(websocket.open)
#     # if not websocket.open:
#     #     break
#         message = output.get()
#         await websocket.send(message)
#     finally:
#         yield from websocket.close()

# TODO a new instance of this is created for each connection - why are messages getting mixed
class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        print("Hey")
        print(hash(self))
        self.randint = random.randint(1, 100)
        print("code - %d", self.randint)
        self.exchange = Exchange(self, self.randint)
        # self.peer.

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

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        print(hash(self))
        print("closing %d", self.randint)
        self.exchange.kill()
        print("closed %d", self.randint)

# start_server = websockets.serve(main, '127.0.0.1', 8081)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8081", debug=False)
    factory.protocol = MyServerProtocol

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
