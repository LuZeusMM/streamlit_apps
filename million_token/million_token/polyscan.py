import numpy as np
import streamlit as st
from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

@dataclass
class PolycanStatistics:
    price_usd: float
    price_eur: float
    price_delta: str
    market_cap: str
    market_cap_f: float
    holders: int


def get_polyscan_output(driver: WebDriver) -> PolycanStatistics:
    polyscan_stats = get_polyscan_stats(driver)
    return polyscan_stats


def display_poly_stats(stats: PolycanStatistics):
    with st.spinner('Loading network statistics'):
        st.title('Polygon Statistics')
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


def get_polyscan_stats(driver: WebDriver) -> PolycanStatistics:
    """ Extracts basic statistical information from Etherscan. """
    driver.get('https://polygonscan.com/token/0x5647Fe4281F8F6F01E84BCE775AD4b828A7b8927')
    current_holders = get_current_holders_poly(driver=driver)
    poly_stats = get_market_values_poly(driver=driver, holders=current_holders)
    poly_stats.holders = current_holders
    return poly_stats


def get_current_holders_poly(driver: WebDriver) -> int:
    """ Returns the number of current holders on the Ethereum network. """
    current_holders = driver.find_element(By.CLASS_NAME, 'mr-3').text.split()[0].replace(',', '')
    return int(current_holders)


def get_market_values_poly(driver, holders: int) -> PolycanStatistics:
    """ Returns the current market values of Million Token. """
    market_values = []
    for elem in driver.find_elements(By.XPATH, '//span[@class = "d-block"]'):
        market_values.append(elem.text)

    price_usd = float(market_values[0].split()[0][1:].replace(',', ''))
    price_increase = market_values[0].split()[4][1:-1].replace(',', '')
    market_cap = float(market_values[1][1:].replace(',', ''))

    poly_stats = PolycanStatistics(price_usd=price_usd,
                                   price_eur=np.round(price_usd * 0.8843, 2),
                                   price_delta=price_increase,
                                   market_cap=str('$' + str(np.round(market_cap/1000000, 2)) + 'M'),
                                   market_cap_f=market_cap,
                                   holders=holders)
    return poly_stats
