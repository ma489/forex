from fx.sim.exchange.OrderDao import OrderDao
from fx.sim.exchange.OrderMatcher import OrderMatcher

orderDao = OrderDao()
orderMatcher = OrderMatcher(orderDao)

order = None  # TODO read from message queue
# TODO update UI with new order

matched = orderMatcher.match(order)

if matched:
    pass  # TODO update UI
else:
    orderDao.persist(order)  # TODO if not, persist to mongo DB with other yet-unmatched orders
