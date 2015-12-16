import shortuuid


class Order:
    def __init__(self, order_type, order_price, order_size, order_conditions):
        self.order_type = order_type
        self.order_price = order_price
        self.order_size = order_size
        self.order_conditions = order_conditions
        self.order_id = shortuuid.ShortUUID().random(length=10)  # Obviously not suitable in the real-world

    def __str__(self):
        string = "Order"
        string += ":\n Type: " + self.order_type.name
        if self.order_price == -1:
            string += ",\n Price: N/A"
        else:
            string += ",\n Price: %f" % self.order_price
        string += ",\n Size: %d" % self.order_size
        string += ",\n Conditions: " + self.order_conditions.name
        string += ",\n OrderID: " + str(self.order_id)
        return string
