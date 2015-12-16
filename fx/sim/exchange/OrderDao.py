class OrderDao(object):
    def __init__(self):
        self.orders = []

    def persist(self, order):
        self.orders.append(order)

    def contains(self, order):
        return order in self.orders

    def remove(self, order):
        pass

    def retrieveAllOrders(self):
        return self.orders
