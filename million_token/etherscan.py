import numpy as np
import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from dataclasses import dataclass
from scrap_token_values import find_price_values
from scrap_token_values import find_market_cap

@dataclass
class EtherscanStatistics:
    price_usd: float
    price_eur: float
    price_delta: str
    market_cap: str
    market_cap_f: float
    holders: int


def get_etherscan_output() -> EtherscanStatistics:
    etherscan_stats = get_etherscan_stats()
    return etherscan_stats


def display_eth_stats(stats: EtherscanStatistics):
    with st.spinner('Loading network statistics'):
        st.title('Ethereum Statistics')
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
            "To see the chart, click [here](https://www.defined.fi/eth/0x24dbedb4699eb996a8ceb2baef4a4ae057cf0294?cache=1c067)")


def get_etherscan_stats() -> EtherscanStatistics:
    """ Extracts basic statistical information from Etherscan. """
    current_holders = get_current_holders_eth()
    etherscan_stats = get_market_values_eth(holders=current_holders)
    etherscan_stats.holders = current_holders
    return etherscan_stats


def get_current_holders_eth() -> int:
    """ Returns the number of current holders on the Ethereum network. """
    url = 'https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611'
    request = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(request, timeout=20).read()
    soup = BeautifulSoup(response, 'html.parser')
    holders = soup.find('div', class_='mr-3')
    current_holders = holders.text.split()[0].replace(',', '')
    return int(current_holders)


def get_market_values_eth(holders: int) -> EtherscanStatistics:
    """ Returns the current market values of Million Token. """
    url = 'https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611'
    req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(req, timeout=20).read()

    price_usd, price_increase = find_price_values(response=response)
    market_cap = find_market_cap(response=response)

    etherscan_stats = EtherscanStatistics(price_usd=price_usd,
                                          price_eur=np.round(price_usd * 0.8843, 2),
                                          price_delta=price_increase,
                                          market_cap=str(
                                              '$' + str(np.round(market_cap / 1000000, 2)) + 'M'),
                                          market_cap_f=market_cap,
                                          holders=holders)
    return etherscan_stats


