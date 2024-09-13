import pandas as pd
import backtrader as bt
import requests
import os
from fintechff_indicator.feeds.MyFeed import MyFeed
import pytz

__ALL__ = ['TestFeed']

class TestFeed(MyFeed):
    params = (
        ('volume', 'vol'),
        ('openinterest', None),
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:1680')}/symbol/info/list"),
        ('params', None),
        ('start_time', None),
        ('end_time', None),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1)
    )

    def __init__(self):
        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        self.fetch_and_process_data()
        super(TestFeed, self).__init__()

    def fetch_and_process_data(self):
        if self.p.url is None or self.p.start_time is None or self.p.end_time is None or self.p.symbol is None:
            raise ValueError("Missing required parameters")

        params = {
            'startTime': self.p.start_time,
            'endTime': self.p.end_time,
            'symbol': self.p.symbol
        }

        response = requests.post(self.p.url, params=params).json()
        if response.get('code') != '200':
            raise ValueError(f"API request failed: {response}")
        
        results = response.get('results')
        if not results:
            raise ValueError("No data returned in the results")

        first_time_close = pd.to_datetime(results[0]['timeClose'], unit='ms')

        cst_tz = pytz.timezone('Asia/Shanghai')
        
        end_time_str = self.p.end_time  # 假设格式为 'yyyy-MM-dd HH:mm:ss'
        end_time_cst = pd.to_datetime(end_time_str).tz_localize(cst_tz)  # 将其转换为东8区

        end_time_timestamp = int(end_time_cst.timestamp() * 1000)

        full_time_range = pd.date_range(
            start=first_time_close.tz_localize('UTC').tz_convert(cst_tz),  # 第一个元素的时间，转换到东8时区
            end=end_time_cst,  # 终止时间为东8时区的 end_time
            freq='1T'  # 按分钟间隔，按需求调整
        )

        # 找出现有数据的时间点，并确保都转换为东8区时间
        existing_times = set(pd.to_datetime([item['timeClose'] for item in results], unit='ms')
                            .tz_localize('UTC').tz_convert(cst_tz))

        # 找出缺失的时间点
        missing_times = [time for time in full_time_range if time not in existing_times]

        # 插入缺失时间点的数据，使用默认值
        for missing_time in missing_times:
            # 创建包含默认值的新数据项
            new_entry = {
                "type": "1",
                "symbol": self.p.symbol,
                "timeClose": int(missing_time.timestamp() * 1000),  # 转换为毫秒时间戳
                "open": 0,  # 默认值
                "close": 0,  # 默认值
                "high": 0,  # 默认值
                "low": 0,  # 默认值
                "vol": 0,  # 默认值
                "turnover": 0,  # 默认值
                "timeOpen": int(missing_time.timestamp() * 1000),  # 默认与 timeClose 相同
                "updateTime": int(missing_time.timestamp()),  # 默认 updateTime
                "bidSize": 0,  # 默认值
                "askSize": 0,  # 默认值
                "premium": 0,  # 默认值
                "volumeDischarge": 0,  # 默认值
                "amountRatio": None  # 默认值
            }

            # 将新数据项添加到 results 列表开头
            results.insert(0, new_entry)

        # 重新排序，保持时间戳倒序排列
        results.sort(key=lambda x: x['timeClose'], reverse=True)
        df = pd.DataFrame(response['results'])

        df.sort_values(by=['timeClose', 'updateTime'], ascending=[True, False], inplace=True)
        df = df.drop_duplicates(subset=['timeClose'], keep='first')

        df['timeClose'] = pd.to_datetime(df['timeClose'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(None)
        df.set_index('timeClose', inplace=True)
        df.sort_index(inplace=True)

        self.p.dataname = df

    def _loadline(self, linetokens):
        return super()._loadline(linetokens)
    


    # def _load(self):
    #     print(f"TestFeed, _load: {datetime.datetime.now()}")
    #     return super()._load()