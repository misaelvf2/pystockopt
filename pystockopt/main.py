import time

import requests_cache
import yfinance as yf
from datetime import date, timedelta
import option as opt
import position as pos
import riskprofile as rp
from stock import Stock

my_session = requests_cache.CachedSession('yfinance.cache')

my_stock = Stock("MSFT", my_session)
my_position = pos.Position(my_stock, 10, "long")
print(my_position.cost_basis)
print(my_position.risk_profile)
