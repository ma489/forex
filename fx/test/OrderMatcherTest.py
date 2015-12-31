import unittest
from queue import Queue, PriorityQueue
from fx.exchangesim.exchange.OrderMatcher import OrderMatcher
from fx.exchangesim.model.Order import Order
from fx.exchangesim.model.OrderConditions import OrderConditions
from fx.exchangesim.model.OrderType import OrderType


class OrderMatcherTest(unittest.TestCase):
    def testLimitBuyAtMarket(self):
        new_order = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Sell, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, 1.6, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        actual_match = order_matcher.match(new_order)
        expected_match = existing_order_1
        self.assertEqual(expected_match, actual_match)

    def testLimitBuyAboveMarketWithPricePrecedence(self):  # marketable limit order
        new_order = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Sell, 1.6, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, 1.5, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        actual_match = order_matcher.match(new_order)
        self.assertEqual(existing_order_2, actual_match)

    def testLimitBuyBelowMarket(self):
        new_order = Order(OrderType.Buy, 1.4, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Sell, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, 1.6, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        expected_match = None
        actual_match = order_matcher.match(new_order)
        self.assertEqual(expected_match, actual_match)

    def testLimitSellAtMarket(self):
        new_order = Order(OrderType.Sell, 1.5, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, 1.6, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testLimitSellAboveMarketWithPricePrecedence(self):
        new_order = Order(OrderType.Sell, 1.6, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, 1.6, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testLimitSellAboveMarket(self):
        new_order = Order(OrderType.Sell, 1.7, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, 1.6, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = None
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testBuyMatchMarketOrdersTimePrecedence(self):
        new_order = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 2)
        existing_order_2 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_1
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testSellMatchMarketOrdersTimePrecedence(self):
        new_order = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 2)
        existing_order_2 = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        expected_match = existing_order_1
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchBuyMarketSellLimitPricePrecedence(self):
        new_order = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Sell, 1.6, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, 1.5, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchSellMarketBuyLimitPricePrecedence(self):
        new_order = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Buy, 1.6, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_1
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchSellMarketBuyMarketOverLimit(self):
        new_order = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 2)
        existing_order_2 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_1
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchSellMarketBuyMarketOverLimitEvenWithTimePrecedence(self):
        new_order = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchSellLimitBuyMarketOverLimitEvenWithTimePrecedence(self):
        new_order = Order(OrderType.Sell, 1.5454, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5353, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchSellLimitBuyMarketOverLimitEvenWithTimePrecedenceAndSamePrice(self):
        new_order = Order(OrderType.Sell, 1.5454, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Buy, 1.5454, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Buy, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.buy_orders.append(existing_order_1)
        order_matcher.buy_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchBuyLimitSellMarketOverLimitEvenWithTimePrecedence(self):
        new_order = Order(OrderType.Buy, 1.5454, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Sell, 1.5353, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)

    def testMatchBuyLimitSellMarketOverLimitEvenWithTimePrecedenceAndSamePrice(self):
        new_order = Order(OrderType.Buy, 1.5454, 1, OrderConditions.Limit, 1)
        existing_order_1 = Order(OrderType.Sell, 1.5454, 1, OrderConditions.Limit, 2)
        existing_order_2 = Order(OrderType.Sell, -1, 1, OrderConditions.Market, 3)
        order_matcher = OrderMatcher(Queue())
        order_matcher.sell_orders.append(existing_order_1)
        order_matcher.sell_orders.append(existing_order_2)
        expected_match = existing_order_2
        actual_match = order_matcher.match(new_order)
        self.assertEqual(actual_match, expected_match)
