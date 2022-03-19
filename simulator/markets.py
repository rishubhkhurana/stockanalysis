from typing import List, Union
import pandas as pd
import numpy as np


class MarketSimulator:

    def __init__(self,
                 df: pd.DataFrame,
                 transaction_cost: float = 0.,
                 slippage: float = 0.1,
                 available_assets: List = ['BTC', 'ETH'],
                 ):
        if not isinstance(df.index, pd.DatetimeIndex):
            raise AttributeError("DataFrame doesn't have datetime index")
        self.df = df
        self.transaction_cost = transaction_cost
        self.slippage = slippage / 100.  # to convert from %
        self.available_assets = available_assets

    def sell_asset(self, asset, row):
        # To Do: trade on next open. For now, adding slippage
        if asset not in self.available_assets:
            raise ValueError(
                f"provide asset not available in the current market. Please choose from one of {self.available_assets}")
        close_price = row['close']
        transaction_cost = self.transaction_cost
        # adding random slippage between 0.05% to 0.1% of slippage
        slippage = np.random.uniform(low=self.slippage / 2, high=self.slippage)
        trade_price = close_price * (1 - slippage)
        return trade_price, transaction_cost

    def buy_asset(self, asset, row):
        # To Do: trade on next open. For now, adding slippage
        if asset not in self.available_assets:
            raise ValueError(
                f"provide asset not available in the current market. Please choose from one of {self.available_assets}")
        close_price = row['close']
        transaction_cost = self.transaction_cost
        # adding random slippage between 0.05% to 0.1% of slippage
        slippage = np.random.uniform(low=self.slippage / 2, high=self.slippage)
        trade_price = close_price * (1 + slippage)
        return trade_price, transaction_cost

    def start_market(self, start):
        self.simulator = self.df.loc[start:].iterrows()

    def next_time(self):
        return next(self.simulator)

    def __iter__(self):
        self.start_market(self.df.index[0])
        while True:
            try:
                yield self.next_time()
            except StopIteration:
                print("Simulation ended!")
                break
