import csv
from datetime import datetime

from pymongo import MongoClient

from fx.historicvis import Tick

#Read file
CURRENCY_PAIR = 'GBPUSD'
FORMATTED_CURRENCY_PAIR = 'GBP/USD'
FILE = '/home/mansour/dev/trading-sim/fx/data/sample/DAT_ASCII_%s_T_201511.csv' % CURRENCY_PAIR

tickList = []
print("Reading...")
#https://docs.python.org/3/library/time.html#time.strftime
with open(FILE, 'r') as csvfile:
    tickReader = csv.reader(csvfile, delimiter='\n')
    for row in tickReader:
        entry = row[0].split(" ")
        date = entry[0]
        formattedDate=datetime.strptime(date, '%Y%m%d')
        formattedDateString = formattedDate.strftime('%d-%b-%Y')
        data = entry[1].split(",")
        time = data[0]
        formattedTime = datetime.strptime(time, '%H%M%S%f')
        formattedTimeString = formattedTime.strftime('%H:%M:%S.%f')
        dateAndTime = formattedDateString + " " + formattedTimeString
        bid = data[1]
        ask = data[2]
        tick = Tick.Tick(FORMATTED_CURRENCY_PAIR, dateAndTime, bid, ask)
        tickList.append(tick)
print("Done.")
print("Size: ")
print(len(tickList))
print(tickList[0])
print(tickList[0].toDict())

#Save to MongoDB
client = MongoClient() #localhost:27017
db = client['local'] #db name 'local'
print("Retrieving tick data...")
print(db.collection_names(include_system_collections=False))
tick_data = db['tick_data'] #collection 'tick_data'
print(tick_data)
print("Saving tick data")
records = [x.toDict() for x in tickList]
print(len(records))
print("Inserting...")
tick_data.insert_many(records)
print(db.collection_names(include_system_collections=False))
print("Retrieving first 'record'...")
print(tick_data.find_one())

tick_data.createIndex(("DateTime",1)) #TODO is this right?