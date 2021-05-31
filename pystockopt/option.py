from datetime import date
import yfinance as yf
from security import Security
OPTION_TYPES = ['call', 'put']


class Option(Security):
    def __init__(self, contract_symbol=None, ticker=None, opt_type=None, premium=None, strike=None, expiration=None,
                 _session=None):
        if contract_symbol:
            self.contract_symbol = contract_symbol
            self._init_from_contract_symbol()
        elif ticker and opt_type and premium and strike and expiration:
            if opt_type not in OPTION_TYPES:
                raise ValueError
            self.ticker = ticker
            self.opt_type = opt_type
            self.premium = premium
            self.strike = strike
            self.purchase_price = self.premium * 100
            self.expiration = expiration
            self._underlying = yf.Ticker(self.ticker)
            self.contract_symbol = self._construct_contract_symbol()
            if self.opt_type == 'call':
                _option_chain = self._underlying.option_chain()
                _calls = _option_chain.calls
                # self._option = _calls[_calls['contractSymbol'] == self.contract_symbol]
            elif self.opt_type == 'put':
                _option_chain = self._underlying.option_chain()
                _puts = _option_chain.puts
                # self._option = _puts[_puts['contractSymbol'] == self.contract_symbol]
        else:
            raise TypeError("Specify contract symbol or manually specify all parameters")

    def _init_from_contract_symbol(self):
        self.ticker, self.expiration, self.opt_type = self._parse_contract_symbol()
        self._underlying = yf.Ticker(self.ticker)
        if self.opt_type == 'call':
            _option_chain = self._underlying.option_chain()
            _calls = _option_chain.calls
            self._option = _calls[_calls['contractSymbol'] == self.contract_symbol]
        elif self.opt_type == 'put':
            _option_chain = self._underlying.option_chain()
            _puts = _option_chain.puts
            self._option = _puts[_puts['contractSymbol'] == self.contract_symbol]
        if self.opt_type not in OPTION_TYPES:
            raise ValueError
        self.premium = self._option['lastPrice'][0]
        self.strike = self._option['strike'][0]
        self.purchase_price = self.premium * 100

    def _parse_contract_symbol(self):
        ticker_end_idx = self._find_ticker()
        ticker = self.contract_symbol[:ticker_end_idx]
        _, ticker, rest = self.contract_symbol.partition(ticker)
        expiration, opt_type_symbol, strike = rest.partition('C')
        if not opt_type_symbol:
            expiration, opt_type_symbol, strike = rest.partition('P')
        if opt_type_symbol == 'C':
            opt_type = 'call'
        else:
            opt_type = 'put'
        expiration = self._parse_expiration(expiration)
        return ticker, expiration, opt_type

    def _construct_contract_symbol(self):
        pass

    def _find_ticker(self):
        idx = 0
        while not self.contract_symbol[idx].isdigit():
            idx += 1
        return idx

    @staticmethod
    def _parse_expiration(expiration):
        year, month, day = int('20' + expiration[:2]), int(expiration[2:4]), int(expiration[4:6])
        return date(year, month, day)

    @property
    def current_price(self):
        return self._option['lastPrice']

    def __repr__(self):
        return f"<ticker: {self.ticker}, type: {self.opt_type}, premium: {self.premium}, strike: {self.strike}, " \
               f"expiration: {self.expiration}>"
