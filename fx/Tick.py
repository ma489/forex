class Tick:
    def __init__(self, currencypair, date, time, bid, ask):
        self.currencyPair = currencypair
        self.date = date
        self.time = time
        self.bid = bid
        self.ask = ask

    def __str__(self):
        string = "Tick"
        string += "\n Pair: " + self.currencyPair
        string += "\n Date: " + self.date
        string += "\n Time: " + self.time
        string += "\n Bid: " + self.bid
        string += "\n Ask: " + self.ask
        return string