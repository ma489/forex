from fx.sim.model.Order import Order
from fx.sim.trader.generators.OrderConditionsGenerator import OrderConditionsGenerator
from fx.sim.trader.generators.OrderPriceGenerator import PriceGenerator
from fx.sim.trader.generators.OrderSizeGenerator import OrderSizeGenerator
from fx.sim.trader.generators.OrderTypeGenerator import OrderTypeGenerator


class OrderGenerator:
    def __init__(self, min_ask, max_ask, min_bid, max_bid):
        self.price_gen = PriceGenerator(min_ask, max_ask, min_bid, max_bid)
        self.size_gen = OrderSizeGenerator()
        self.type_gen = OrderTypeGenerator()
        self.cond_gen = OrderConditionsGenerator()

    def generateOrder(self, minAsk, maxAsk, minBid, maxBid):
        order_price = self.price_gen.generateAskPrice()
        order_size = self.size_gen.generateOrderSize()
        order_type = self.type_gen.generateOrderType()
        order_conditions = self.cond_gen.generateOrderConditions()
        order = Order(order_type, order_price, order_size, order_conditions)
        return order
