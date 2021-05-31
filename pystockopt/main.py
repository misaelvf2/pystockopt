import time

import requests_cache
import yfinance as yf
from datetime import date, timedelta
from position import Position
import riskprofile as rp
from stock import Stock
from option import Option

my_session = requests_cache.CachedSession('yfinance.cache')

my_stock = Stock("MSFT", my_session)
my_option = Option("PLTR", "call", 3.59, 25.00, date(2022, 1, 21), my_session)

my_position = Position(my_option, 1, "long")
print(my_option)
print(my_position.profit)

# my_position = pos.Position(my_stock, 10, "long")
# print(my_position.cost_basis)
# print(my_position.risk_profile)
