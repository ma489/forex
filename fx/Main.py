from bottle import route, run, static_file, response
from fx.web.RetrieveData import RetrieveData
from bson.json_util import dumps

RD = RetrieveData()

@route('/')
def main():
    return static_file('index.html', 'web/static/')

@route('/historic/<currency_pair>')
def historic(currency_pair='None'):
    result = RD.retrieve(currency_pair)
    response.content_type = 'application/json'
    return dumps(result)

#Run server
run(host='localhost', port=8080, debug=True)