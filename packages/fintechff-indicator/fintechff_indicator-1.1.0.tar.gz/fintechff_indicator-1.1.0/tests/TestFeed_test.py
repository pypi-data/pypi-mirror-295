import backtrader as bt
from fintechff_indicator.feeds.TestFeed import TestFeed
from fintechff_indicator.brokers.TradingView import TradingView
import pytz

class SimpleStrategy(bt.Strategy):
    def __init__(self):
        super(SimpleStrategy, self).__init__()
        self.cache = {}
        self.tv = TradingView()

    def next(self):
        bar_datetime = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f")
        # print(f"datetime: {bar_datetime}, open: {self.data.open[0]}, high: {self.data.high[0]}, low: {self.data.low[0]}, close: {self.data.close[0]}")

        # print(f"close[0]: {self.data.close[0]}, close[-1]: {self.data.close[-1]}")
        if self.data.close[0] > self.data.close[-1]:
            self.buy()
        if self.data_close[0] < self.data_close[-1]:
            self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # my_data = MyLiveFeed(symbol="CAPITALCOM:HK50")
    my_data = TestFeed(symbol="CAPITALCOM:HK50", start_time="2024-09-09 15:00:00", end_time="2024-09-10 01:00:00")
    cerebro.adddata(my_data)

    cerebro.addstrategy(SimpleStrategy)

    cerebro.broker.setcash(10000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run(runonce=False)
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()