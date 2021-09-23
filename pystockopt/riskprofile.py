import math
from pystockopt.option import Option
from pystockopt.stock import Stock


class RiskProfile:
    def __init__(self, security, quantity, outlook):
        self.outlook = outlook
        self.quantity = quantity
        self.security = security
        self._set_profile()

    def _set_profile(self):
        self._profile = {
            'breakeven': 0.0,
            'max_profit': 0.0,
            'max_loss': 0.0,
        }
        if isinstance(self.security, Option):
            if self.security.opt_type == 'call':
                if self.outlook == 'long':
                    self._profile['breakeven'] = self.security.strike + \
                        self.security.premium
                    self._profile['max_profit'] = math.inf
                    self._profile['max_loss'] = - \
                        self.security.premium * self.quantity * 100
                elif self.outlook == 'short':
                    self._profile['breakeven'] = self.security.strike + \
                        self.security.premium
                    self._profile['max_profit'] = self.security.premium * \
                        self.quantity * 100
                    self._profile['max_loss'] = -math.inf
            elif self.security.opt_type == 'put':
                if self.outlook == 'long':
                    pass
                elif self.outlook == 'short':
                    pass
        elif isinstance(self.security, Stock):
            if self.outlook == 'long':
                self._profile['breakeven'] = self.security.purchase_price
                self._profile['max_profit'] = math.inf
                self._profile['max_loss'] = self.security.purchase_price * \
                    self.quantity
            elif self.outlook == 'short':
                self._profile['breakeven'] = self.security.purchase_price
                self._profile['max_profit'] = self.security.purchase_price * \
                    self.quantity
                self._profile['max_loss'] = -math.inf

    @property
    def profile(self):
        return self._profile

    def profit(self, price):
        if self.security.opt_type == 'call':
            if self.outlook == 'long':
                return max(price - self._profile['breakeven'],
                           self._profile['max_loss'])
            elif self.outlook == 'short':
                return min(self._profile['breakeven'] - price,
                           self._profile['max_profit'])
        elif self.security.opt_type == 'put':
            if self.outlook == 'long':
                pass
            elif self.outlook == 'short':
                pass
