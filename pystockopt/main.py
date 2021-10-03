from pystockopt import position
import time
from rich import print, inspect
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

import requests_cache
import yfinance as yf
from datetime import date, timedelta
from pystockopt import option
from pystockopt.option import Option

ITERATION = 0


def test_y_finance():
    my_ticker = yf.Ticker("PLTR")
    return my_ticker.info


def test_options():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option("PLTR", "call", 3.59, 25.00,
                       date(2022, 1, 21), my_session)
    return my_option.build_contract_symbol()


def generate_table() -> Table:
    # my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=None)

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
        (f"[bold green]{percent_change}"
         if my_option.percent_change >= 0
         else f"[bold red]{percent_change}"),
        my_option.opt_type.capitalize(),
        str(my_option.premium),
        str(my_option.strike),
        str(my_option.expiration)
    )

    return table


def generate_table_1() -> Table:
    # my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=None)

    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("Contract")
    table.add_column("Ticker")
    table.add_column("Last Price")
    table.add_column("% Change")
    table.add_column("Type")
    table.add_column("Iteration")

    last_price = my_option.last_price
    percent_change = my_option.percent_change
    global ITERATION
    ITERATION += 1

    table.add_row(
        my_option.symbol,
        my_option.ticker,
        str(last_price),
        (f"[bold green]{percent_change}"
         if my_option.percent_change >= 0
         else f"[bold red]{percent_change}"),
        my_option.opt_type.capitalize(),
        str(ITERATION)
    )

    return table


def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    layout["upper"].update(generate_table())
    layout["lower"].update(generate_table_1())
    return layout


def main():
    with Live(make_layout(), refresh_per_second=10) as live:
        while True:
            time.sleep(1)
            live.update(make_layout())


def test():
    my_session = requests_cache.CachedSession('yfinance.cache')
    my_option = Option(ticker="PLTR", opt_type="call", premium=3.59,
                       strike=25.00, expiration=date(2022, 1, 21),
                       _session=my_session)

    inspect(Option.get_options_chain_from_yf(
        my_option.stock, my_option.expiration), methods=True)


if __name__ == "__main__":
    main()
    # test()
