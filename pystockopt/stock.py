import yfinance as yf
from pystockopt.utils import get_ticker_from_yf
from pystockopt.security import Security
from datetime import date


class Stock(Security):
    def __init__(self, ticker, price=None, _session=None):
        self.ticker = ticker
        self._stock = get_ticker_from_yf(ticker, _session)
        self.purchase_price = price

    @property
    def last_price(self):
        return self._stock.info['regularMarketPrice']

    @property
    def percent_change(self):
        previous_close = self._stock.info['previousClose']
        percent_change = (self.last_price - previous_close) / \
            previous_close * 100
        return percent_change

    @property
    def stock(self):
        return self._stock

    @property
    def company(self):
        return self._stock.info['shortName']

    def price_range(self, start, end):
        start_price = self.price_on(start)
        end_price = self.price_on(end)
        return end_price - start_price

    def price_on(self, date):
        price_history = self.stock.history(start=date)
        price_on_date = price_history.loc[str(date)]["Close"]
        return price_on_date

    def max_price_range(self, start, end):
        price_history = self.stock.history(start=start, end=end)
        max_price = price_history["Close"].max()
        min_price = price_history["Close"].min()
        return max_price - min_price

    def max_price_range_percent(self, start, end):
        price_history = self.stock.history(start=start, end=end)
        max_price = price_history["Close"].max()
        min_price = price_history["Close"].min()
        return 100 * (max_price - min_price) / ((max_price + min_price) / 2)

    def __repr__(self):
        return f"<ticker: {self.ticker}, \
             current price: {self.last_price}>"


if __name__ == "__main__":
    my_stock = Stock(ticker="PLTR")
    price_range = my_stock.price_range(
        start=date(2021, 4, 28), end=date(2021, 10, 28))
    max_price_range = my_stock.max_price_range(
        start=date(2021, 4, 1), end=date(2021, 10, 28))
    print(f"Price range: {price_range}")
    print(f"Max price range: {max_price_range}")
