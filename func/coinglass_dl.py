from pprint import pprint
import argparse

from cybotrade.permutation import Permutation
from cybotrade.runtime import Runtime
from cybotrade.runtime import StrategyTrader
from cybotrade.strategy import Strategy as BaseStrategy
from cybotrade.models import (
    OrderParams,
    OrderSide,
    RuntimeMode,
    RuntimeConfig,
    Exchange,
)
from datetime import datetime, timedelta, timezone

import asyncio
import pandas as pd
import logging
# import colorlog
from numpy import int64

class Strategy(BaseStrategy):
    datasource_data = []
    start_time = datetime.now(timezone.utc) # datetime.utcnow()
    async def on_datasource_interval(self, strategy: StrategyTrader, topic: str):
        # logging.info("datasource data {}".format(super().data_map[topic][-1]))
        super().data_map[topic][-1]['date'] = datetime.fromtimestamp(int(super().data_map[topic][-1]['start_time'])/1000)
        self.datasource_data.append(super().data_map[topic][-1])

    async def on_backtest_complete(self, strategy: StrategyTrader):
        df = pd.DataFrame(self.datasource_data)
        df.to_csv(f"{coin}.csv")
        time_taken = datetime.now(timezone.utc) - self.start_time
        print("Total time taken: ", time_taken)

def get_lsur_per(ticker):
    config = RuntimeConfig(
    mode=RuntimeMode.Backtest,
    candle_topics=[],
    datasource_topics=[f"coinglass|1m|futures/globalLongShortAccountRatio/history?exchange=Binance&symbol={ticker}USDT&interval=1h"],
    start_time = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    end_time = datetime(2024, 4, 1, 0, 0, 0, tzinfo=timezone.utc),
    data_count = 4500,
    api_key = "test",
    api_secret = "notest",
    active_order_interval=1,
    initial_capital=10_000.0,
    )
    permutation = Permutation(config)
    return permutation

async def start_backtest(ticker):
    hyper_parameters = {}
    await get_lsur_per(ticker).run(hyper_parameters, Strategy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', type=str, default="BTC", help="Symbol that will download")

    args = parser.parse_args()
    coin = args.symbol
    asyncio.run(start_backtest(coin))
