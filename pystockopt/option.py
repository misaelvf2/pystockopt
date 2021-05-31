from security import Security
OPTION_TYPES = ['call', 'put']


class Option(Security):
    def __init__(self, ticker, opt_type, premium, strike, expiration, _session):
        self.ticker = ticker
        if opt_type not in OPTION_TYPES:
            raise ValueError
        self.opt_type = opt_type
        self.premium = premium
        self.purchase_price = premium * 100
        self.strike = strike
        self.expiration = expiration

    @property
    def current_price(self):
        return self._stock.info['regularMarketPrice']

    def __repr__(self):
        return f"<ticker: {self.ticker}, type: {self.opt_type}, premium: {self.premium}, strike: {self.strike}, expiration: {self.expiration}>"
