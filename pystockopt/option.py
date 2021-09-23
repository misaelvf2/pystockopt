from pystockopt.security import Security

import yfinance as yf

OPTION_TYPES = ['call', 'put']


class Option(Security):
    def __init__(self, ticker=None, opt_type=None, premium=None,
                 strike=None, expiration=None, _session=None):
        self.ticker = ticker
        if opt_type not in OPTION_TYPES:
            raise ValueError
        self._stock = yf.Ticker(ticker, session=_session)
        self.opt_type = opt_type
        self.premium = premium
        self.purchase_price = premium * 100
        self.strike = strike
        self.expiration = expiration

    def build_contract_symbol(self):
        contract_symbol = ''
        contract_symbol = self.ticker + self.expiration.strftime("%y%m%d")
        contract_symbol += 'C' if self.opt_type == 'call' else 'P'

        strike_component = str(int(self.strike * 1000))
        strike_component = '0' * (8 - len(strike_component)) + strike_component
        contract_symbol += strike_component
        return contract_symbol

    @property
    def current_price(self):
        pass

    def __repr__(self):
        return f"<ticker: {self.ticker}, type: {self.opt_type}, \
            premium: {self.premium}, strike: {self.strike}, \
            expiration: {self.expiration}>"
