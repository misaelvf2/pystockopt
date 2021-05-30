import yfinance as yf
from security import  Security


class Stock(Security):
    def __init__(self, ticker, _session):
        self.ticker = ticker
        self._stock = yf.Ticker(ticker, session=_session)
        self.purchase_price = self._stock.info['regularMarketPrice']
