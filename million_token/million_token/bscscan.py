import numpy as np
import streamlit as st
from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@dataclass
class BscscanStatistics:
    price_usd: float
    price_eur: float
    price_delta: str
    market_cap: str
    market_cap_f: float
    holders: int


def get_bscscan_output(driver: WebDriver, display=True) -> BscscanStatistics:
    bscscan_stats = get_bsc_stats(driver=driver)

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
        st.subheader("To see the chart, click [here](https://www.defined.fi/bsc/0x7cb5e7048215f7c225a8248b4c33fd32ca579c75?cache=6ad2c)")


def get_bsc_stats(driver: WebDriver) -> BscscanStatistics:
    """ Extracts basic statistical information from Etherscan. """
    driver.get('https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4')
    current_holders = get_current_holders_bsc(driver=driver)
    etherscan_stats = get_market_values_bsc(driver=driver, holders=current_holders)
    etherscan_stats.holders = current_holders
    return etherscan_stats


def get_current_holders_bsc(driver: WebDriver) -> int:
    """ Returns the number of current holders on the Ethereum network. """
    current_holders = driver.find_element(By.CLASS_NAME, 'mr-3').text.split()[0].replace(',', '')
    return int(current_holders)


def get_market_values_bsc(driver, holders: int) -> BscscanStatistics:
    """ Returns the current market values of Million Token. """
    market_values = []
    for elem in driver.find_elements(By.XPATH, '//span[@class = "d-block"]'):
        market_values.append(elem.text)

    price_usd = float(market_values[0].split()[0][1:].replace(',', ''))
    price_increase = market_values[0].split()[4][1:-1].replace(',', '')
    market_cap = float(market_values[1][1:].replace(',', ''))

    etherscan_stats = BscscanStatistics(price_usd=price_usd,
                                        price_eur=np.round(price_usd * 0.8843, 2),
                                        price_delta=price_increase,
                                        market_cap=str('$' + str(np.round(market_cap/1000000, 2)) + 'M'),
                                        market_cap_f=market_cap,
                                        holders=holders)
    return etherscan_stats
