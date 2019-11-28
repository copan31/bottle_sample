#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
from bottle import route, run, template, request, static_file, TEMPLATE_PATH
from StockManagerDBHelper import *

logging.basicConfig(level=logging.DEBUG)

# localhost:8080
@route('/')
def title():
    return template('manager')

@route('/css/<filename>')
def css_dir(filename):
    css = static_file(filename, root='./static/css')
    return css

@route('/js/<filename>')
def js_dir(filename):
    js = static_file(filename, root='./static/js')
    return js

@route('/fonts/<filename>')
def fonts_dir(filename):
    fonts = static_file(filename, root='./static/fonts')
    return fonts

# localhost:8080/show
@route('/data', method='GET')
def data():
    obj = StockManagerDBHelper.makeJsonData()
    return obj

# localhost:8080/show
@route('/buy', method='GET')
def buy():
    code = request.query.code
    price = request.query.price
    count = request.query.count
    date = request.query.date
    reason = request.query.reason
    obj = StockManagerDBHelper.saveBuyData(code, price, count, date, reason)
    return obj

# localhost:8080/show
@route('/sell', method='GET')
def sell():
    buy_id = request.query.buy_id
    price = request.query.price
    count = request.query.count
    date = request.query.date
    reason = request.query.reason
    obj = StockManagerDBHelper.saveSellData(buy_id, price, count, date, reason)
    return obj

# ビルドインサーバの実行
run(host='localhost', port=8080, debug=True, reloader=True)
