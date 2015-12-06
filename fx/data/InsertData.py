import csv
from datetime import datetime
from fx import Tick

#https://docs.python.org/3/library/time.html#time.strftime

CURRENCY_PAIR = 'GBPUSD'
FILE = '/home/mansour/dev/trading-sim/fx/data/sample/DAT_ASCII_%s_T_201511.csv' % CURRENCY_PAIR

tickList = []
print("Reading...")
with open(FILE, 'r') as csvfile:
    tickReader = csv.reader(csvfile, delimiter='\n')
    #print("Currency Pair:" + CURRENCY_PAIR)
    i = 0
    for row in tickReader:
        entry = row[0].split(" ")
        date = entry[0]
        formattedDate=datetime.strptime(date, '%Y%m%d')
        formattedDateString = formattedDate.strftime('%d-%b-%Y')
        data = entry[1].split(",")
        time = data[0]
        formattedTime = datetime.strptime(time, '%H%M%S%f')
        formattedTimeString = formattedTime.strftime('%H:%M:%S.%f')
        bid = data[1]
        ask = data[2]
        tick = Tick.Tick(CURRENCY_PAIR, formattedDateString, formattedTimeString, bid, ask)
        tickList.append(tick)
print("Done.")
print("Size: " + len(tickList))
print(tickList[0])