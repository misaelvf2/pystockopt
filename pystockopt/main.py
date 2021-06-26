import time

import requests_cache
import yfinance as yf
from datetime import date, timedelta
from position import Position
import riskprofile as rp
from stock import Stock
from option import Option


def test_y_finance():
    my_ticker = yf.Ticker("PLTR")
    return my_ticker.option_chain('2022-01-21')

def test_options():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option("PLTR", "call", 3.59, 25.00, date(2022, 1, 21), my_session)
    return my_option.build_contract_symbol()

result = test_y_finance()
print(result)
