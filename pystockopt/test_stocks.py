from yfinance import ticker
from pystockopt.stock import Stock
import unittest
import requests_cache
from datetime import date, timedelta
from numpy.testing import assert_almost_equal


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
        params = [(date(2021, 1, 5), date(2021, 2, 6), None, 24.14),
                  (date(2021, 1, 5), None, "1mo", 24.14)]

        for param in params:
            start, end, period, expected = param
            with self.subTest(msg=f"start={start}, end={end}, period={period}"):
                result = self.my_stock.price_change(
                    start=start, end=end, period=period)
                self.assertAlmostEqual(result, expected, places=2)

    def test_price_range(self):
        params = [(date(2021, 10, 5), date(2021, 11, 6), None, 47.68),
                  (date(2021, 10, 5), None, "1mo", 47.68)]

        for param in params:
            start, end, period, expected = param
            with self.subTest(msf=f"start={start}, end={end}, period={period}"):
                result = self.my_stock.price_range(
                    start=start, end=end, period=period)
                self.assertAlmostEqual(result, expected, places=2)

    def test_price_range_percent(self):
        result = self.my_stock.price_range_percent(
            start=date(2021, 10, 5), end=date(2021, 11, 5)
        )
        self.assertAlmostEqual(result, 15.25, places=2)

    def test_price_range_values(self):
        params = [(date(2021, 10, 5), date(2021, 11, 6), None, (288.76, 336.44)),
                  (date(2021, 10, 5), None, "1mo", (288.76, 336.44))]

        for param in params:
            start, end, period, expected = param
            with self.subTest(msf=f"start={start}, end={end}, period={period}"):
                result = self.my_stock.price_range_values(
                    start=start, end=end, period=period)
                assert_almost_equal(result, expected, decimal=2)

    if __name__ == "__main__":
        unittest.main()
