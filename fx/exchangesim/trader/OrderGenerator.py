from fx.exchangesim.model.Order import Order
from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType
from fx.exchangesim.trader.OrderConditionsGenerator import OrderConditionsGenerator
from fx.exchangesim.trader.OrderPriceGenerator import PriceGenerator
from fx.exchangesim.trader.OrderSizeGenerator import OrderSizeGenerator
from fx.exchangesim.trader.OrderTypeGenerator import OrderTypeGenerator


class OrderGenerator:
    def __init__(self, min_ask, max_ask, min_bid, max_bid):
        self.price_gen = PriceGenerator(min_ask, max_ask, min_bid, max_bid)
        self.size_gen = OrderSizeGenerator()
        self.type_gen = OrderTypeGenerator()
        self.cond_gen = OrderConditionsGenerator()

    def generateOrder(self, orderid):
        order_size = self.size_gen.generateOrderSize()
        order_type = self.type_gen.generateOrderType()
        order_conditions = self.cond_gen.generateOrderConditions()
        if order_conditions == OrderConditions.Market:
            order_price = -1
        else: #TODO AHHHH
            if order_type is OrderType.Buy:
                order_price = self.price_gen.generateBidPrice()
            else:
                order_price = self.price_gen.generateAskPrice()
        order = Order(order_type, order_price, order_size, order_conditions, orderid)
        return order
