# -*- coding: utf-8 -*-

from flow import *
from flask import Flask
from datetime import datetime

app = Flask(__name__)
netprefix = '192.168.1.'
today = datetime.today()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api')
def apilist():
    '''Return docs for api methods'''
    return 'API helper'

@app.route('/api/traf/', defaults={'direction':'in', 'month':today.month, 'year':today.year,'ip':netprefix})
@app.route('/api/traf/<direction>/', defaults={'month':today.month, 'year':today.year,'ip':netprefix})
@app.route('/api/traf/<direction>/<int:month>/', defaults={'year':today.year,'ip':netprefix})
@app.route('/api/traf/<direction>/<int:month>/<int:year>/', defaults={'ip':netprefix})
@app.route('/api/traf/<direction>/<int:month>/<int:year>/<ip>')
def traf(direction,month,year,ip):
    out = ''
    for x in getmonthreport(month,year,direction,ip):
        out += ' '.join(x) + '\n'
    return out

if __name__ == '__main__':
    app.run()

