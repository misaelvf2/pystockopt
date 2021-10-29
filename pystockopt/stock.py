import yfinance as yf
from pystockopt.utils import get_ticker_from_yf
from pystockopt.security import Security


class Stock(Security):
    def __init__(self, ticker, price, _session):
        self.ticker = ticker
        self._stock = get_ticker_from_yf(ticker, _session)
        self.purchase_price = price

    @property
    def last_price(self):
        return self._stock.info['regularMarketPrice']

    @property
    def percent_change(self):
        previous_close = self._stock.info['previousClose']
        percent_change = (self.last_price - previous_close) / previous_close * 100
        return percent_change

    @property
    def stock(self):
        return self._stock

    @property
    def company(self):
        return self._stock.info['shortName']

    def __repr__(self):
        return f"<ticker: {self.ticker}, \
             current price: {self.last_price}>"
