import math


class RiskProfile:
    def __init__(self, trade):
        self.outlook = trade.outlook
        self.option = trade.option
        self._set_profile()

    def _set_profile(self):
        self._profile = {
            'breakeven': 0.0,
            'max_profit': 0.0,
            'max_loss': 0.0,
        }
        if self.option.opt_type == 'call':
            if self.outlook == 'long':
                self._profile['breakeven'] = self.option.strike + self.option.premium
                self._profile['max_profit'] = math.inf
                self._profile['max_loss'] = -self.option.premium
            elif self.outlook == 'short':
                self._profile['breakeven'] = self.option.strike + self.option.premium
                self._profile['max_profit'] = self.option.premium
                self._profile['max_loss'] = -math.inf
        elif self.option.opt_type == 'put':
            if self.outlook == 'long':
                pass
            elif self.outlook == 'short':
                pass

    @property
    def profile(self):
        return self._profile

    def profit(self, price):
        if self.option.opt_type == 'call':
            if self.outlook == 'long':
                return max(price - self._profile['breakeven'], self._profile['max_loss'])
            elif self.outlook == 'short':
                return min(self._profile['breakeven'] - price, self._profile['max_profit'])
        elif self.option.opt_type == 'put':
            if self.outlook == 'long':
                pass
            elif self.outlook == 'short':
                pass
