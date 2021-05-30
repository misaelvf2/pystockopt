OUTLOOKS = ["long", "short"]


class Trade:
    def __init__(self, option, outlook):
        self.option = option
        if outlook not in OUTLOOKS:
            raise ValueError
        self.outlook = outlook
