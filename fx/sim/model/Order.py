class Order:

    def __init__(self, order_type, order_price, order_size, order_conditions):
        self.order_type = order_type
        self.order_price = order_price
        self.order_size = order_size
        self.order_conditions = order_conditions

    def __str__(self):
        string = "Order"
        string += ":\n Type: " + self.order_type.name
        string += ",\n Price: %f" % self.order_price
        string += ",\n Size: %d" % self.order_size
        string += ",\n Conditions: " + self.order_conditions.name
        return string
