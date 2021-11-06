"""
Contains classes for representing and manipulating stocks
"""

import datetime
from dateutil.relativedelta import relativedelta
from pystockopt.utils import get_ticker_from_yf
from pystockopt.security import Security

# 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y
PERIOD_TO_RELATIVEDELTA = {
    "1d": relativedelta(days=1),
    "5d": relativedelta(days=5),
    "1mo": relativedelta(months=1),
    "3mo": relativedelta(months=3),
    "6mo": relativedelta(months=6),
    "1y": relativedelta(years=1),
    "2y": relativedelta(years=2),
    "5y": relativedelta(years=5),
    "10y": relativedelta(years=10),
}


class Stock(Security):
    def __init__(self, ticker, price=None, _session=None):
        self.ticker = ticker
        self._stock = get_ticker_from_yf(ticker, _session)
        self.purchase_price = price

    @property
    def last_price(self):
        return self._stock.info['regularMarketPrice']

    @property
    def change(self):
        previous_close = self._stock.info['previousClose']
        change = self.last_price - previous_close
        return change

    @property
    def percent_change(self):
        previous_close = self._stock.info['previousClose']
        percent_change = (self.last_price - previous_close) / \
            previous_close * 100
        return percent_change

    @property
    def stock(self):
        """Reference to underlying stock ticker from yf."""
        return self._stock

    @property
    def company(self):
        """Returns the stock's company name."""
        return self._stock.info['shortName']

    def price_change(self, start, end=None, period="1mo"):
        """Returns change in price from given dates."""
        price_history = self.stock.history(start=start, end=end)
        start_price = price_history.loc[str(start)]["Close"]
        if end:
            end = end - relativedelta(days=1)
        else:
            if period == "ytd":
                end = datetime.date.today() - relativedelta(days=1)
            else:
                end = start + PERIOD_TO_RELATIVEDELTA[period]
        end_price = price_history.loc[str(end)]["Close"]
        return end_price - start_price

    def price_on(self, date):
        """Returns price on given date."""
        price_history = self.stock.history(start=date)
        price_on_date = price_history.loc[str(date)]["Close"]
        return price_on_date

    def price_range_values(self, start, end):
        """Returns tuple consisting of the low and high values of the price range for a given time period."""
        price_history = self.stock.history(start=start, end=end)
        max_price = price_history["Close"].max()
        min_price = price_history["Close"].min()
        return (min_price, max_price)

    def price_range(self, start, end):
        """Returns the price range for given time period."""
        price_history = self.stock.history(start=start, end=end)
        max_price = price_history["Close"].max()
        min_price = price_history["Close"].min()
        return max_price - min_price

    def price_range_percent(self, start, end):
        """Returns price range for given time period as percentage."""
        price_history = self.stock.history(start=start, end=end)
        max_price = price_history["Close"].max()
        min_price = price_history["Close"].min()
        return 100 * (max_price - min_price) / ((max_price + min_price) / 2)

    def save_price_history(self, start, end=None, period="1mo"):
        """Saves price history of stock for given time period."""
        price_history = self.stock.history(start=start, end=end)
        price_history.to_csv(f"{self.ticker}_price_history_{start}.csv")

    def __repr__(self):
        """String representation of Stock object."""
        return f"<ticker: {self.ticker}, \
             current price: {self.last_price}>"


if __name__ == "__main__":
    my_stock = Stock(ticker="MSFT")
    price_change = my_stock.price_change(
        start=datetime.date(2021, 1, 5), period="1mo")

    print(f"Price change: {price_change}")

    # my_stock.save_price_history(start=datetime.date(
    #     2021, 1, 5), end=datetime.date(2021, 2, 6))
