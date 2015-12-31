import csv
import calendar
import os
from datetime import datetime

from pymongo import MongoClient

from fx.historicvis.model import Tick

month_lookup = {v: k for k,v in enumerate(calendar.month_abbr)}

#Read file
CURRENCY_PAIR = 'GBPUSD' # GBPJPY
FORMATTED_CURRENCY_PAIR = 'GBP/USD' #GBP/JPY
FILE = os.getcwd() + 'fx/historicvis/data/samplesource/DAT_ASCII_%s_T_201511.csv' % CURRENCY_PAIR
tickList = []
print("Reading...")


def get_date_object(date_and_time):
    #e.g. 01-Nov-2015 17:00:43.990000
    day = date_and_time[0:2]
    month = date_and_time[3:6]
    month = month_lookup.get(month)
    year = date_and_time[7:11]
    hour = date_and_time[12:14]
    minute = date_and_time[15:17]
    second = date_and_time[18:20]
    sub_second = date_and_time[21:28]
    return datetime(int(year), month, int(day), int(hour), int(minute), int(second), int(sub_second))


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
        dateTimeObject = get_date_object(dateAndTime)
        tick = Tick.Tick(FORMATTED_CURRENCY_PAIR, dateTimeObject, bid, ask)
        tickList.append(tick)
print("Done.")
print("Size: ")
print(len(tickList))

#Save to MongoDB
client = MongoClient() #localhost:27017
db = client['local'] #db name 'local'
print("Retrieving tick data...")
print(db.collection_names(include_system_collections=False))
tick_data = db['tick_data'] #collection 'tick_data'
# print(tick_data)
print("Saving tick data")
records = [x.toDict() for x in tickList]
print(len(records))
print("Inserting...")
tick_data.insert_many(records)
print(db.collection_names(include_system_collections=False))
print("Retrieving first 'record'...")

#Note: When setting up, create index in MongoDB: db.getCollection('tick_data').createIndex({DateTime:1})
