import yfinance as yf


def get_ticker_from_yf(ticker, session):
    return yf.Ticker(ticker, session)
