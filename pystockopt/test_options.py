from yfinance import ticker
from pystockopt.option import Option
import unittest
import requests_cache
from datetime import date, timedelta


class TestOptions(unittest.TestCase):

    def setUp(self):
        self.my_session = requests_cache.CachedSession('yfinance.cache')
        self.my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                                strike=25.00, expiration=date(2022, 1, 21),
                                _session=self.my_session)

    def test_options_symbol(self):
        self.assertEqual(self.my_option.build_contract_symbol(),
                         "PLTR220121C00025000")

    def test_price(self):
        self.assertTrue(self.my_option.last_price)

    if __name__ == "__main__":
        unittest.main()
