from pystockopt import position
import time
from rich import print, inspect
from rich.console import Console
from rich.table import Table

import requests_cache
import yfinance as yf
from datetime import date, timedelta
from pystockopt import option
from pystockopt.option import Option


def test_y_finance():
    my_ticker = yf.Ticker("PLTR")
    return my_ticker.info


def test_options():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option("PLTR", "call", 3.59, 25.00,
                       date(2022, 1, 21), my_session)
    return my_option.build_contract_symbol()


def main():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=my_session)

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Ticker", width=12)
    table.add_column("Type")
    table.add_column("Premium")
    table.add_column("Strike")
    table.add_column("Expiration")

    table.add_row(
        my_option.ticker,
        my_option.opt_type,
        str(my_option.premium),
        str(my_option.strike),
        str(my_option.expiration)
    )

    console.print(table)


if __name__ == "__main__":
    main()
