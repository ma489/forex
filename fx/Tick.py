#The minimum upward or downward movement in the price of a security.
#The term "tick" also refers to the change in the price of a security from trade to trade.
#Since 2001, with the advent of decimalization, the minimum tick size for stocks trading above $1 is 1 cent.
class Tick:
    def __init__(self, currencypair, datetime, bid, ask):
        self.currencyPair = currencypair
        self.dateTime = datetime
        self.bid = bid
        self.ask = ask

    def __str__(self):
        string = "Tick"
        string += "\n Pair: " + self.currencyPair
        string += "\n DateTime: " + self.dateTime
        string += "\n Bid: " + self.bid
        string += "\n Ask: " + self.ask
        return string

    def toDict(self):
        return {"Pair" : self.currencyPair,
                "DateTime" : self.dateTime,
                "Bid" : self.bid,
                "Ask" : self.ask }