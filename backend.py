from flask import Flask, render_template, request, flash, redirect, jsonify
from config import BinanceConfig, FlaskConfig
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
app.secret_key = FlaskConfig['Secret']

client = Client(BinanceConfig['Key'], BinanceConfig['Secret'])

@app.route('/')
def index():
    title = 'Trading Algo'
    
    account = client.get_account()

    balances = account['balances']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render_template('index.html', title=title, my_balances=balances, symbols=symbols)

@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'], 
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'], 
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/history')
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jul, 2020", "12 Jul, 2020")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)
    
    del candlestick, candlesticks

    return jsonify(processed_candlesticks)

if __name__=="__main__":
    app.run(debug=True)