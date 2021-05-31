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
my_option1 = Option("PLTR210604C00010000")
my_option2 = Option(ticker="PLTR", opt_type="call", premium=12.05, strike=10.0, expiration=date(2021, 6, 4))

my_position1 = Position(my_option1, 1, "long")
my_position2 = Position(my_option2, 1, "long")

print(my_position1)
print(my_position2)
# print(my_position.profit)

# my_position = pos.Position(my_stock, 10, "long")
# print(my_position.cost_basis)
# print(my_position.risk_profile)
