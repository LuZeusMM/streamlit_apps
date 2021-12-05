import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from selenium import webdriver
from dataclasses import dataclass
from etherscan import get_etherscan_output
from bscscan import get_bscscan_output
from polyscan import get_polyscan_output
from etherscan import EtherscanStatistics
from bscscan import BscscanStatistics
from polyscan import PolycanStatistics
from etherscan import display_eth_stats
from bscscan import display_bsc_stats
from polyscan import display_poly_stats
from all_networks import get_all_networks_output
from PIL import Image
from selenium.webdriver.firefox.options import Options
firefox_options = Options()
firefox_options.add_argument("--headless")


@dataclass
class Statistics:
    etherscan_stats: EtherscanStatistics
    bscscan_stats: BscscanStatistics
    polyscan_stats: PolycanStatistics


def show_statistics(newtwork_option: str, stats: Statistics):
    if newtwork_option == 'Ethereum':
        display_eth_stats(stats.etherscan_stats)
    elif newtwork_option == 'Binance Smart Chain':
        display_bsc_stats(stats.bscscan_stats)
    elif newtwork_option == 'Polygon Network':
        display_poly_stats(stats.polyscan_stats)


def show_statistics_all_networks(statistics: Statistics):
    network_data_combined = get_all_networks_output(statistics)
    total_mc = network_data_combined['Market Capitalization'].sum()
    display_total_mc = str('$' + str(np.round(total_mc/1000000, 2)) + 'M')
    total_holders = network_data_combined['Holders'].sum()
    market_cap_column, holders_column = st.columns(2)
    market_cap_column.metric(label='Total Market Capitalization', value=display_total_mc)
    holders_column.metric(label='Holders', value=int(total_holders))


@st.cache
def get_statistics_from_all_networks() -> Statistics:
    driver = webdriver.Firefox(options=firefox_options)
    etherscan_stats = get_etherscan_output(driver)
    bscscan_stats = get_bscscan_output(driver)
    polyscan_stats = get_polyscan_output(driver)
    statistics = Statistics(etherscan_stats=etherscan_stats,
                            bscscan_stats=bscscan_stats,
                            polyscan_stats=polyscan_stats)
    return statistics


def main():
    statistics = get_statistics_from_all_networks()

    mm_logo = Image.open('../images/MM_logo.png')
    st.image(mm_logo)

    network_options = np.array(['Ethereum', 'Binance Smart Chain', 'Polygon Network'])
    network_option = st.selectbox(label='Choose network', options=network_options, index=0)
    show_statistics(newtwork_option=network_option, stats=statistics)

    st.title('Networks combined')
    show_statistics_all_networks(statistics)

    html_file_markets = open("markets_component.html", 'r', encoding='utf-8')
    source_code_markets = html_file_markets.read()

    st.subheader("Buy Million Token here")
    components.html(source_code_markets)

    st.subheader("For more information, visit [milliontoken.org](https://www.milliontoken.org/)")


if __name__ == '__main__':
    main()
