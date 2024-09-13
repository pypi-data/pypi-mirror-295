import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone

__ALL__ = ['MyFeed']

class MyFeed(bt.feeds.DataBase):
    params = (
        ('volume', 'vol'),
        ('openinterest', None),
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:1680')}/symbol/info/list"),
        ('start_time', None),
        ('end_time', None),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('debug', False)
    )

    def __init__(self):
        if self.p.url is None or self.p.start_time is None or self.p.end_time is None or self.p.symbol is None:
            raise ValueError("Missing required parameters")

        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        super(MyFeed, self).__init__(fromdate=datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0),
                                      todate=datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0))
        self.cache = {}

    def _load(self):
        start_time = None
        if self.lines.datetime.idx == 0:
            start_time = datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
        else:
            start_time = self.lines.datetime.datetime(-1).replace(tzinfo=timezone.utc).astimezone() + timedelta(minutes=1)

        end_time = start_time + timedelta(minutes=1)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        if start_time.timestamp() >= datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0).timestamp():
            return False

        key = f"{self.p.symbol}_{start_time_str}_{end_time_str}"
        if key not in self.cache:
            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol
            }

            if self.p.debug:
                print(f"MyFeed, fetch data params: {params}")

            response = requests.post(self.p.url, params=params).json()
            if self.p.debug:
                print(f"MyFeed, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")
            
            results = response.get('results', [])
            if len(results) > 0:
                self.cache[key] = results[0]
                
        bar = self.cache.get(key, None)
        if bar is not None:
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeOpen'] / 1000.0, timezone.utc))
            self.lines.open[0] = bar['open']
            self.lines.high[0] = bar['high']
            self.lines.low[0] = bar['low']
            self.lines.close[0] = bar['close']
            self.lines.volume[0] = bar['vol']
            return True