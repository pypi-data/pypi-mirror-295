import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta

__ALL__ = ['LongTermDirection']

class LongTermDirection(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('ltd',)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.247:8220')}/signal/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('backpeek_size', 3),
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
                print(f"LongTermDirection, fetch data params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                print(f"LongTermDirection, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            if len(response['results']) > 0:
                self.cache[current_bar_time_str] = self.NA
                for result in response['results']:
                    if result['longTermDir'] == 'BULLISH':
                        self.cache[current_bar_time_str] = self.BULLISH
                    elif result['longTermDir'] == 'BEARISH':
                        self.cache[current_bar_time_str] = self.BEARISH

                    if self.p.debug:
                        print(f"LongTermDirection, current_bar_time_str: {current_bar_time_str}, long_term_dir: {result['longTermDir']}")

        self.lines.ltd[0] = self.cache.get(current_bar_time_str, self.NA)