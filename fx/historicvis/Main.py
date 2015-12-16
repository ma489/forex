import calendar

import time
from bottle import route, run, static_file, response
from bson.json_util import dumps

from fx.historicvis.web.RetrieveData import RetrieveData

RD = RetrieveData()

@route('/')
def main():
    return static_file('index.html', 'historicvis/web/static/')

@route('/historic/<currency_pair>')
def historic(currency_pair='None'):
    result = RD.retrieve(currency_pair)
    response.content_type = 'application/json'
    return dumps(result)

@route('/exchange')
def main():
    return static_file('Exchange.html', 'historicvis/web/static/')

#Run server
#run(host='localhost', port=8080, debug=True)
run(host='localhost', port=8080, server='paste')