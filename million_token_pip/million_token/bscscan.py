from urllib.request import Request, urlopen
import numpy as np
import streamlit as st
from dataclasses import dataclass
from bs4 import BeautifulSoup
from scrap_token_values import find_price_values
from scrap_token_values import find_market_cap


@dataclass
class BscscanStatistics:
    price_usd: float
    price_eur: float
    price_delta: str
    market_cap: str
    market_cap_f: float
    holders: int


def get_bscscan_output() -> BscscanStatistics:
    bscscan_stats = get_bsc_stats()
    return bscscan_stats


def display_bsc_stats(stats: BscscanStatistics):
    with st.spinner('Loading network statistics'):
        st.title('Binance Smart Chain Statistics')
        price_usd_column, price_eur_column, market_cap_column, holders_column = st.columns(4)
        price_usd_column.metric(label='Price ($)',
                                value=stats.price_usd,
                                delta=stats.price_delta)
        price_eur_column.metric(label='Price (€)',
                                value=stats.price_eur,
                                delta=stats.price_delta)
        market_cap_column.metric(label='Market Capitalization',
                                 value=stats.market_cap)
        holders_column.metric(label='Holders', value=stats.holders)
        st.subheader(
            "To see the chart, click [here](https://www.defined.fi/bsc/0x7cb5e7048215f7c225a8248b4c33fd32ca579c75?cache=6ad2c)")


def get_bsc_stats() -> BscscanStatistics:
    """ Extracts basic statistical information from Etherscan. """
    current_holders = get_current_holders_bsc()
    bscscan_stats = get_market_values_bsc(holders=current_holders)
    bscscan_stats.holders = current_holders
    return bscscan_stats


def get_current_holders_bsc() -> int:
    """ Returns the number of current holders on the Ethereum network. """
    url = 'https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4'
    request = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(request, timeout=20).read()
    soup = BeautifulSoup(response, 'html.parser')
    holders = soup.find('div', class_='mr-3')
    current_holders = holders.text.split()[0].replace(',', '')
    return int(current_holders)


def get_market_values_bsc(holders: int) -> BscscanStatistics:
    """ Returns the current market values of Million Token. """
    url = 'https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4'
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(req, timeout=20).read()

    price_usd, price_increase = find_price_values(response=response)
    market_cap = find_market_cap(response=response)

    bscscan_stats = BscscanStatistics(price_usd=price_usd,
                                      price_eur=np.round(price_usd * 0.8843, 2),
                                      price_delta=price_increase,
                                      market_cap=str(
                                          '$' + str(np.round(market_cap / 1000000, 2)) + 'M'),
                                      market_cap_f=market_cap,
                                      holders=holders)
    return bscscan_stats



