OUTLOOKS = ["long", "short"]


class Position:
    def __init__(self, security, outlook):
        self.security = security
        if outlook not in OUTLOOKS:
            raise ValueError
        self.outlook = outlook
