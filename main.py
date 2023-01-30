import requests
import json
from kucoin.client import Client
import os
import ccxt
import pandas as pd
from decimal import Decimal
import time
from datetime import datetime


api_key = "635b91ace4743e0001ca260f"
api_secret = "2de78a92-9d17-4ffb-8e97-601bcfc14afc"
api_passphrase = "idk85625881IDK!"

client = Client(api_key, api_secret, api_passphrase)


exchange = ccxt.binance({
    'rateLimit': 2000,
    'enableRateLimit': True,
})


# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# requesting data from url
data = requests.get(key)
data = data.json()
# print(f"{data['symbol']} price is {data['price']}")
btc_price = data['price']
print(btc_price)
print(type(float(btc_price)))


# order = client.create_market_order('BTC-USDT', Client.SIDE_BUY, size=0.0001)
account = client.get_accounts()
print(account[3])
print(account[4])
if account[3]["currency"] == "USDT" and account[4]["currency"] == "BTC":
    # number 4 is bitcoin
    btc_balance = account[4]["balance"]
    value_of_btc_in_account = Decimal(btc_balance) * Decimal(btc_price)
    usdt_in_account = account[3]["balance"]
    total_balance = Decimal(usdt_in_account) + value_of_btc_in_account
elif account[4]["currency"] == "BTC" and account[3]["currency"] == "USDT":
    btc_balance = account[4]["balance"]
    value_of_btc_in_account = Decimal(btc_balance) * Decimal(btc_price)
    usdt_in_account = account[3]["balance"]
    total_balance = Decimal(usdt_in_account) + value_of_btc_in_account
elif account[3]["currency"] == "BTC" and account[4]["currency"] == "USDT":
    btc_balance = account[3]["balance"]
    value_of_btc_in_account = Decimal(btc_balance) * Decimal(btc_price)
    usdt_in_account = account[4]["balance"]
    total_balance = Decimal(usdt_in_account) + value_of_btc_in_account
else:
    print("Acount list numbers have changed.")

print(total_balance)

# Upload total_balance data to thingspeak.
api_key_thingspeak = 'Z7E32G7OH55VXQQU'
channel_id = '2008467'
field = '4'
data = total_balance
url = 'https://api.thingspeak.com/update?api_key=' + \
    api_key_thingspeak + '&field' + field + '=' + str(data)

# comment out uploads.
#response = requests.get(url)
# print(response.status_code)

read_api_key = 'WZNRSUTOIH9PHQNC'

# url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results=20'
# response = requests.get(url)
# data = response.json()
# data1 = data['feeds']

# print(type(data1))
# print(type(data1[0]))

# data2 = data1[0]
# # print(data2)
# print(data1)
# predicted_high = data2["field2"]
# predicted_low = data2["field1"]

# get latest data

url = 'https://api.thingspeak.com/channels/' + \
    channel_id + '/feeds/last.json?api_key=' + read_api_key
response = requests.get(url)
data = response.json()

print(url)
print("The data is", data)
print(data["field1"])

if data["field1"] > btc_price:
    # Good forecast show green LED
    print('Good forecast')
    forecast = 1
else:
    # Bad forecast show red LED
    print('Bad forecast')
    forecast = 0

# wait for button to be pressed.
# If button is pressed


def whenBuzzerPressed():
    print('buzzerPressed')
    if forecast == 1:
        order = client.create_market_order(
            'BTC-USDT', Client.SIDE_BUY, size=0.0001)
        # Beep buzzer.
        # Get the current time in UTC
        now = datetime.utcnow()

        # Check if it is 12 am
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            marketClosed = 1
        else:
            marketClosed = 0

        while btc_price < data['field2'] and marketClosed == 0:
            print('price has not hit target')
            time.sleep(10)
            now = datetime.utcnow()
            if now.hour == 0 and now.minute == 0 and now.second == 0:
                marketClosed = 1
            else:
                marketClosed = 0
        order = client.create_market_order(
            'BTC-USDT', Client.SIDE_SELL, size=0.0001)
    if forecast == 0:
        order = client.create_market_order(
            'BTC-USDT', Client.SIDE_SELL, size=0.0001)
        now = datetime.utcnow()

        # Check if it is 12 am
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            marketClosed = 1
        else:
            marketClosed = 0
        while btc_price > data['field3'] and marketClosed == 0:
            print("low has not been reached")
            now = datetime.utcnow()
            time.sleep(10)
            if now.hour == 0 and now.minute == 0 and now.second == 0:
                marketClosed = 1
            else:
                marketClosed = 0
        if marketClosed == 0:
            print('Low has reached')
            order = client.create_market_order(
                'BTC-USDT', Client.SIDE_BUY, size=0.0001)
        while checkIfMarketClosed() == 0:
            time.sleep(30)
        order = client.create_market_order(
            'BTC-USDT', Client.SIDE_SELL, size=0.0001)


def checkIfMarketClosed():
    now = datetime.utcnow()
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        marketClosed = 1
        return marketClosed
    else:
        marketClosed = 0
        return marketClosed
