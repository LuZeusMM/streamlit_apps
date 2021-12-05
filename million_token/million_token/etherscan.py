import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@dataclass
class EtherscanStatistics:
    price_usd: float
    price_eur: float
    price_delta: str
    market_cap: str
    market_cap_f: float
    holders: int


def get_etherscan_output(driver: WebDriver) -> EtherscanStatistics:
    etherscan_stats = get_etherscan_stats(driver=driver)
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
        st.subheader("To see the chart, click [here](https://www.defined.fi/eth/0x24dbedb4699eb996a8ceb2baef4a4ae057cf0294?cache=1c067)")


def get_etherscan_stats(driver: WebDriver) -> EtherscanStatistics:
    """ Extracts basic statistical information from Etherscan. """
    driver.get('https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611')
    current_holders = get_current_holders_eth(driver=driver)
    etherscan_stats = get_market_values_eth(driver=driver, holders=current_holders)
    etherscan_stats.holders = current_holders
    return etherscan_stats


def get_current_holders_eth(driver: WebDriver) -> int:
    """ Returns the number of current holders on the Ethereum network. """
    current_holders = driver.find_element(By.CLASS_NAME, 'mr-3').text.split()[0].replace(',', '')
    return int(current_holders)


def get_market_values_eth(driver, holders: int) -> EtherscanStatistics:
    """ Returns the current market values of Million Token. """
    market_values = []
    for elem in driver.find_elements(By.XPATH, '//span[@class = "d-block"]'):
        market_values.append(elem.text)

    price_usd = float(market_values[0].split()[0][1:].replace(',', ''))
    price_increase = market_values[0].split()[4][1:-1].replace(',', '')
    market_cap = float(market_values[1][1:].replace(',', ''))

    etherscan_stats = EtherscanStatistics(price_usd=price_usd,
                                          price_eur=np.round(price_usd * 0.8843, 2),
                                          price_delta=price_increase,
                                          market_cap=str('$' + str(np.round(market_cap/1000000, 2)) + 'M'),
                                          market_cap_f=market_cap,
                                          holders=holders)
    return etherscan_stats
