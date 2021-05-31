import yfinance as yf
from security import  Security


class Stock(Security):
    def __init__(self, ticker, _session):
        self.ticker = ticker
        self._stock = yf.Ticker(ticker, session=_session)
        self.purchase_price = self._stock.info['regularMarketPrice']

    @property
    def current_price(self):
        return self._stock.info['regularMarketPrice']

    def __repr__(self):
        return f"<ticker: {self.ticker}, purchase price: {self.purchase_price}, current price: {self.current_price}>"
