import pandas as pd
from etherscan import EtherscanStatistics
from bscscan import BscscanStatistics
from polyscan import PolycanStatistics
from dataclasses import dataclass


@dataclass
class Statistics:
    etherscan_stats: EtherscanStatistics
    bscscan_stats: BscscanStatistics
    polyscan_stats: PolycanStatistics


def get_all_networks_output(statistics: Statistics) -> pd.DataFrame:
    network_data_combined = pd.DataFrame({'Price': [statistics.etherscan_stats.price_usd,
                                                    statistics.bscscan_stats.price_usd,
                                                    statistics.polyscan_stats.price_usd],
                                          'Market Capitalization': [statistics.etherscan_stats.market_cap_f,
                                                                    statistics.bscscan_stats.market_cap_f,
                                                                    statistics.polyscan_stats.market_cap_f],
                                          'Holders': [statistics.etherscan_stats.holders,
                                                      statistics.bscscan_stats.holders,
                                                      statistics.polyscan_stats.holders]},
                                         index=['Ethereum', 'Binance Smart Chain', 'Polygon'])
    return network_data_combined
