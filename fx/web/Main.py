from bottle import route, run, static_file, response
from bson.json_util import dumps
from fx.historicvis.data.RetrieveData import RetrieveData
RD = RetrieveData()


@route('/')
def main():
    return static_file('index.html', 'static/')


@route('/historic/<currency_pair>')
def historic(currency_pair='None'):
    result = RD.retrieve(currency_pair)
    response.content_type = 'application/json'
    return dumps(result)


@route('/exchange')
def main():
    return static_file('Exchange.html', 'static/')


@route('/static/:filename#.*#')
def main(filename):
    return static_file(filename, 'static/')


run(host='localhost', port=8080)
# TODO start trading-sim here too in new thread? Exchange.start()
