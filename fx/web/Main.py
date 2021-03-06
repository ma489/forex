import sys
sys.path.append('/home/mansour/dev/trading-sim')
print(sys.path)

from bottle import route, run, static_file, response
from bson.json_util import dumps
from fx.historicvis.data.RetrieveData import RetrieveData
RD = RetrieveData()


@route('/')
def main():
    return static_file('index.html', 'fx/web/static/')


@route('/historic-vis')
def historicvis():
    return static_file('historic.html', 'fx/web/static/')


@route('/historic/<currency_pair>/<start_date>/<end_date>')
def historic(currency_pair='None', start_date='None', end_date='None'):
    result = RD.retrieve(currency_pair, start_date, end_date)
    response.content_type = 'application/json'
    return dumps(result)


@route('/exchange')
def main():
    return static_file('exchange.html', 'fx/web/static/')


@route('/static/:filename#.*#')
def main(filename):
    return static_file(filename, 'fx/web/static/')

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', 'fx/web/static/')


run(server='paste')
