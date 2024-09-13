import requests
import os
import json

__ALL__ = ['TradingView']

class TradingView:
    def __init__(self, id=None):
        self.base_url = os.environ.get('TRADINGVIEW_BROKER_BASE_URL', 'http://192.168.25.90:3005/book')
        self.id = id if id is not None else os.environ.get('TRADINGVIEW_BROKER_ID', "14078173")

    def _place_order(self, symbol="", type="", side="", qty=0):
        url = f"{self.base_url}?id={self.id}"
        data = {
            "symbol": symbol,
            "type": type,
            "side": side,
            "qty": float(qty)
        }
        payload = f"data={json.dumps(data)}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return requests.post(url, headers=headers, data=payload).json()

    def buy(self, symbol="", type="", qty=0):
        return self._place_order(symbol=symbol, type=type, side="buy", qty=qty)

    def sell(self, symbol="", type="", qty=0):
        return self._place_order(symbol=symbol, type=type, side="sell", qty=qty)