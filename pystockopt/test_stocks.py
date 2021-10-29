from yfinance import ticker
from pystockopt.stock import Stock
import unittest
import requests_cache
from datetime import date, timedelta


class TestStocks(unittest.TestCase):

    def setUp(self):
        self.my_session = requests_cache.CachedSession('yfinance.cache')
        self.my_stock = Stock(
            ticker="MSFT", price=300.00, _session=self.my_session)

    def test_price(self):
        self.assertTrue(self.my_stock.last_price)

    def test_percent_change(self):
        self.assertTrue(self.my_stock.percent_change)

    def test_company(self):
        self.assertTrue(self.my_stock.company)

    if __name__ == "__main__":
        unittest.main()
