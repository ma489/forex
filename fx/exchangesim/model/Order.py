import datetime

class Order:
    def __init__(self, order_type, order_price, order_size, order_conditions, order_id):
        #TODO add currency pair?
        self.order_type = order_type
        self.order_price = order_price
        self.order_size = order_size
        self.remaining_unfilled = order_size
        self.order_conditions = order_conditions
        self.order_id = order_id
        self.entry_time = datetime.datetime.utcnow()

    def __str__(self):
        string = "Order"
        string += ":\n Type: " + self.order_type.name
        if self.order_price == -1.0:
            string += ",\n Price: N/A"
        else:
            string += ",\n Price: %.4f" % self.order_price
        string += ",\n Size: %d" % self.order_size
        string += ",\n Remaining Unfilled: %d" % self.remaining_unfilled
        string += ",\n Conditions: " + self.order_conditions.name
        string += ",\n OrderID: " + str(self.order_id)
        string += ",\n Order Time: " + str(self.entry_time.isoformat())
        return string
