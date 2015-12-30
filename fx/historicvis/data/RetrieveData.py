import datetime
from pymongo import MongoClient


class RetrieveData:
    def __init__(self):
        self.data = []

    def retrieve(self, currency_pair, start_date, end_date):
        client = MongoClient()  # localhost:27017
        db = client['local']  # db name 'local'
        tick_data = db['tick_data']  # collection 'tick_data'
        formatted_currency_pair = currency_pair[0:3] + "/" + currency_pair[3:7]
        print(formatted_currency_pair)
        print(start_date)
        start = self.get_date(start_date)
        print(start)
        end = self.get_date(end_date)
        print(end)
        result = tick_data.find({"Pair": formatted_currency_pair, "DateTime": {"$gte": start, "$lte": end}},
                                {'_id': 0}).sort([("DateTime", 1)])
        return [x for x in result]

    def get_date(self, date):
        # 11/01/2015 5:00 PM
        year = int(date[6:10])
        month = int(date[0:2])
        day = int(date[3:5])
        minute = int(date[13:15])
        hour = int(date[11:12])
        am_pm = date[16:18]
        if am_pm == 'PM':
            hour += 12
        return datetime.datetime(year, month, day, hour, minute, 0, 0)

    def retrieve_all(self, currency_pair):
        client = MongoClient()  # localhost:27017
        db = client['local']  # db name 'local'
        tick_data = db['tick_data']  # collection 'tick_data'
        result = tick_data.find().aggregate([{"$group": {"_id": "$_id", "avgBid": {"$avg": "$Bid"}}}])
        return [x for x in result]
