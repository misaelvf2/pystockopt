from pystockopt.utils import get_ticker_from_yf
from yfinance import ticker
from pystockopt.security import Security
import requests_cache
from datetime import date, timedelta
from pystockopt.utils import get_ticker_from_yf

import yfinance as yf

OPTION_TYPES = ['call', 'put']


class Option(Security):

    def __init__(self, ticker=None, opt_type=None, premium=None, strike=None,
                 expiration=None, contract_size=100, _session=None):
        self.ticker = ticker
        if opt_type not in OPTION_TYPES:
            raise ValueError
        self._stock = get_ticker_from_yf(ticker, _session)
        self.opt_type = opt_type
        self.premium = premium
        self.contract_size = contract_size
        self.purchase_price = premium * contract_size
        self.strike = strike
        self.expiration = expiration
        self._symbol = self.build_contract_symbol()

    @staticmethod
    def get_options_chain_from_yf(stock, date):
        options_chain = stock.option_chain(date=str(date))
        return options_chain

    @staticmethod
    def get_call_options_from_yf(stock, date):
        options_chain = Option.get_options_chain_from_yf(
            stock=stock, date=date)
        return options_chain.calls

    @staticmethod
    def get_put_options_from_yf(stock, date):
        options_chain = Option.get_options_chain_from_yf(
            stock=stock, date=date)
        return options_chain.puts

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
    def stock(self):
        return self._stock

    @property
    def percent_change(self):
        options = self._get_options_from_yf(type=self.opt_type)

        percent_change = options.loc[options['contractSymbol']
                                     == self.symbol, 'percentChange'].values[0]
        return percent_change

    def _get_options_from_yf(self, type):
        options = (
            Option.get_call_options_from_yf(
                stock=self.stock, date=self.expiration)
            if type == 'call'
            else Option.get_put_options_from_yf(
                stock=self.stock, date=self.expiration))
        return options

    def _init_from_contract_symbol(self):
        self.ticker, self.expiration, self.opt_type = (
            self._parse_contract_symbol())
        self._underlying = yf.Ticker(self.ticker)
        if self.opt_type == 'call':
            _option_chain = self._underlying.option_chain()
            _calls = _option_chain.calls
            self._option = _calls[_calls['contractSymbol']
                                  == self.symbol]
        elif self.opt_type == 'put':
            _option_chain = self._underlying.option_chain()
            _puts = _option_chain.puts
            self._option = _puts[_puts['contractSymbol']
                                 == self.symbol]
        if self.opt_type not in OPTION_TYPES:
            raise ValueError
        self.premium = self._option['lastPrice'][0]
        self.strike = self._option['strike'][0]
        self.purchase_price = self.premium * self.contract_size

    def _parse_contract_symbol(self):
        ticker_end_idx = self.ticker
        ticker = self.symbol[:ticker_end_idx]
        _, ticker, rest = self.symbol.partition(ticker)
        expiration, opt_type_symbol, strike = rest.partition('C')
        if not opt_type_symbol:
            expiration, opt_type_symbol, strike = rest.partition('P')
        if opt_type_symbol == 'C':
            opt_type = 'call'
        else:
            opt_type = 'put'
        expiration = self._parse_expiration(expiration)
        return ticker, expiration, opt_type

    @staticmethod
    def _parse_expiration(expiration):
        year, month, day = int(
            '20' + expiration[:2]), int(expiration[2:4]), int(expiration[4:6])
        return date(year, month, day)

    @property
    def last_price(self):
        options = self._get_options_from_yf(type=self.opt_type)

        last_price = options.loc[options['contractSymbol']
                                 == self.symbol, 'lastPrice'].values[0]
        return last_price

    def __repr__(self):
        return f"<ticker: {self.ticker}, type: {self.opt_type}, \
            premium: {self.premium}, strike: {self.strike}, \
            expiration: {self.expiration}>"
