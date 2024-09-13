import backtrader as bt
import pytz
import requests
from datetime import timedelta
from datetime import datetime
import os

__ALL__ = ['TradeAction']

class TradeAction(bt.Indicator):
    (BUY, NA, SELL) = (1, 0, -1)

    lines = ('ta',)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.247:8220')}/signal/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('backpeek_size', 30),
        ('debug', False)
    )

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def next(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_bar_time_str not in self.cache or self.cache[current_bar_time_str] == self.NA:
            start_time_str = (current_bar_time - timedelta(minutes=self.p.backpeek_size)).strftime('%Y-%m-%d %H:%M:%S')
            params = {
                'startTime' : start_time_str,
                'endTime' : current_bar_time.strftime('%Y-%m-%d %H:%M:%S'),
                'symbol' : self.p.symbol
            }

            if self.p.debug:
                print(f"TradeAction, fetch data params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                print(f"TradeAction, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            if len(response['results']) > 0:
                self.cache[current_bar_time_str] = self.NA
                for result in response['results']:
                    if result['tradeAction'] == 'BUY':
                        self.cache[current_bar_time_str] = self.BUY
                    elif result['tradeAction'] == 'SELL':
                        self.cache[current_bar_time_str] = self.SELL
                    
                    if self.p.debug:
                        print(f"TradeAction, current_time_str: {current_bar_time_str}, trade_action: {result['tradeAction']}")

        self.lines.ta[0] = self.cache.get(current_bar_time_str, self.NA)