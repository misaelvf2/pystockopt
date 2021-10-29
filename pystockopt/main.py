# z from pystockopt import position
import time
from rich import print, inspect
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

import requests_cache
import yfinance as yf
from datetime import date, timedelta
from pystockopt.option import Option
from pystockopt.stock import Stock


def test_y_finance():
    my_ticker = yf.Ticker("PLTR")
    return my_ticker.info


def test_options():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option("PLTR", "call", 3.59, 25.00,
                       date(2022, 1, 21), my_session)
    return my_option.build_contract_symbol()


def generate_options_table() -> Table:
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=my_session)

    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("Contract")
    table.add_column("Ticker")
    table.add_column("Last Price")
    table.add_column("% Change")
    table.add_column("Type")
    table.add_column("Premium")
    table.add_column("Strike")
    table.add_column("Expiration")

    last_price = my_option.last_price
    percent_change = my_option.percent_change

    table.add_row(
        my_option.symbol,
        my_option.ticker,
        str(last_price),
        (f"[bold green]{percent_change:.2f}"
         if my_option.percent_change >= 0
         else f"[bold red]{percent_change:.2f}"),
        my_option.opt_type.capitalize(),
        str(my_option.premium),
        str(my_option.strike),
        str(my_option.expiration)
    )

    return table


def generate_stocks_table() -> Table:
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_stock = Stock(ticker="MSFT", price=300.00, _session=None)

    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("Company")
    table.add_column("Ticker")
    table.add_column("Last Price")
    table.add_column("% Change")

    company = my_stock.company
    last_price = my_stock.last_price
    percent_change = my_stock.percent_change

    table.add_row(
        company,
        my_stock.ticker,
        str(last_price),
        (f"[bold green]{percent_change:.2f}"
         if my_stock.percent_change >= 0
         else f"[bold red]{percent_change:.2f}")
    )

    return table


def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    layout["upper"].update(Panel(generate_options_table()))
    layout["lower"].update(Panel(generate_stocks_table()))
    return layout


def main():
    with Live(make_layout(), refresh_per_second=1, screen=True) as live:
        while True:
            time.sleep(1)
            live.update(make_layout())


def test():
    my_session = requests_cache.CachedSession('yfinance.cache')
    # my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
    #                    strike=25.00, expiration=date(2022, 1, 21),
    #                    _session=my_session)

    # inspect(Option.get_options_chain_from_yf(
    #     my_option.stock, my_option.expiration), methods=True)
    my_stock = Stock(ticker="MSFT", price=300.00, _session=None)
    print(my_stock.company)
    # inspect(my_stock._stock, methods=True)


if __name__ == "__main__":
    main()
    # test()
