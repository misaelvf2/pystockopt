from pystockopt.riskprofile import RiskProfile

OUTLOOKS = ["long", "short"]


class Position:
    def __init__(self, security, quantity, outlook):
        self.security = security
        self.quantity = quantity
        if outlook not in OUTLOOKS:
            raise ValueError
        self.outlook = outlook
        self.open = True
        self._set_cost_basis()
        self._set_risk_profile()

    def _set_cost_basis(self):
        self._cost_basis = self.security.purchase_price * self.quantity

    def _set_risk_profile(self):
        self._risk_profile = RiskProfile(
            self.security, self.quantity, self.outlook)

    @property
    def cost_basis(self):
        print(f"<<cost_basis: {self._cost_basis}")
        return self._cost_basis

    @property
    def risk_profile(self):
        return self._risk_profile.profile

    @property
    def profit(self):
        return self.security.current_price - self.cost_basis

    def __repr__(self):
        return f"<Ticker: {self.security.ticker}, Outlook: {self.outlook}, \
                Quantity: {self.quantity}, \
                Cost Basis: {self.cost_basis}>"
