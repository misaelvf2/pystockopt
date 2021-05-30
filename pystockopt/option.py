from security import Security
OPTION_TYPES = ['call', 'put']


class Option(Security):
    def __init__(self, opt_type, premium, strike, expiration):
        if opt_type not in OPTION_TYPES:
            raise ValueError
        self.opt_type = opt_type
        self.premium = premium
        self.strike = strike
        self.expiration = expiration

    def __repr__(self):
        return f"<type: {self.opt_type}, premium: {self.premium}, strike: {self.strike}, expiration: {self.expiration}>"
