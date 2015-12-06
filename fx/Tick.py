#The minimum upward or downward movement in the price of a security.
#The term "tick" also refers to the change in the price of a security from trade to trade.
#Since 2001, with the advent of decimalization, the minimum tick size for stocks trading above $1 is 1 cent.
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

    def toDict(self):
        return {"Pair" : self.currencyPair,
                "Date" : self.date,
                "Time" : self.time,
                "Bid" : self.bid,
                "Ask" : self.bid }