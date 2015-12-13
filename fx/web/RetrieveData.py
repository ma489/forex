from pymongo import MongoClient


class RetrieveData:
    def __init__(self):
        self.data = []

    def retrieve(self, currency_pair):
        client = MongoClient()  # localhost:27017
        db = client['local']  # db name 'local'
        tick_data = db['tick_data']  # collection 'tick_data'
        result = tick_data.find({}, {'_id': 0}).sort([("DateTime", 1)]).limit(250)  # TODO remove limit?
        return [x for x in result]


        # x = RetrieveData()
        # print(x.retrieve())
