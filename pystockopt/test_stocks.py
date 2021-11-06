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

    def test_price_on(self):
        result = self.my_stock.price_on(date(2021, 9, 29))
        self.assertAlmostEqual(result, 284.00, places=2)

    def test_price_change(self):
        result = self.my_stock.price_change(
            start=date(2021, 1, 4), end=date(2021, 9, 29))
        self.assertAlmostEqual(result, 67.24, places=2)

    def test_price_range(self):
        result = self.my_stock.price_range(
            start=date(2021, 10, 5), end=date(2021, 11, 5))
        self.assertAlmostEqual(result, 47.68, places=2)

    def test_price_range_percent(self):
        result = self.my_stock.price_range_percent(
            start=date(2021, 10, 5), end=date(2021, 11, 5)
        )
        self.assertAlmostEqual(result, 15.25, places=2)

    if __name__ == "__main__":
        unittest.main()
