from yfinance import ticker
from pystockopt.security import Security
import requests_cache
from datetime import date, timedelta

import yfinance as yf

OPTION_TYPES = ['call', 'put']


class Option(Security):
    def __init__(self, ticker=None, opt_type=None, premium=None,
                 strike=None, expiration=None, _session=None):
        self.ticker = ticker
        if opt_type not in OPTION_TYPES:
            raise ValueError
        self._stock = self._get_ticker_from_yf(ticker, _session)
        self.opt_type = opt_type
        self.premium = premium
        self.purchase_price = premium * 100
        self.strike = strike
        self.expiration = expiration
        self._symbol = self.build_contract_symbol()

    def _get_ticker_from_yf(self, ticker, session):
        return yf.Ticker(ticker, session)

    def _get_options_chain_from_yf(self, date):
        options_chain = self._stock.option_chain(date=date)
        return options_chain

    def build_contract_symbol(self):
        contract_symbol = ''
        contract_symbol = self.ticker + self.expiration.strftime("%y%m%d")
        contract_symbol += 'C' if self.opt_type == 'call' else 'P'

        strike_component = str(int(self.strike * 1000))
        strike_component = '0' * (8 - len(strike_component)) + strike_component
        contract_symbol += strike_component
        return contract_symbol

    @property
    def symbol(self):
        return self._symbol

    @property
    def last_price(self):
        options_chain = self._get_options_chain_from_yf(
            date=str(self.expiration))
        call_options = options_chain.calls
        last_price = call_options.loc[call_options['contractSymbol']
                                      == self.symbol, 'lastPrice'].values[0]
        return last_price

    def __repr__(self):
        return f"<ticker: {self.ticker}, type: {self.opt_type}, \
            premium: {self.premium}, strike: {self.strike}, \
            expiration: {self.expiration}>"


if __name__ == "__main__":
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=my_session)

    print(my_option.last_price)
