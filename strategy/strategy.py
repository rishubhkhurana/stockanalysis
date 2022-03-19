import numpy as np
import pandas as pd



class StrategyFactory:
    def __init__(self,
                 max_bet_size: float = 1.,
                 min_shares_allowed: float = 1e-4,
                 signal_col: str = 'signal'):
        self.max_bet_size = max_bet_size
        self.min_shares_allowed = min_shares_allowed
        self.signal_col = signal_col

    def get_bet_size(self, *args, **kwargs):
        raise NotImplementedError

    def execute_current_timestamp(self, *args, **kwargs):
        raise NotImplementedError


class LongOnlyStrategy(StrategyFactory):

    def __init__(self, max_bet_size: float = 0.1,
                 min_shares_allowed: float = 1e-4,
                 signal_col: str = 'signal'):
        self.max_bet_size = max_bet_size
        self.min_shares_allowed = min_shares_allowed
        self.signal_col = signal_col

    def execute_current_timestamp(self,
                                  row: pd.DataFrame,
                                  timestamp: Union[pd.Timestamp, datetime],
                                  portfolio: Portfolio,
                                  account: Account,
                                  market: MarketSimulator):
        asset = row['asset']
        if row['signal'] == 'b':
            # print('Buy')
            if portfolio.positions[asset][-1] == 'OOM':
                price, trade_cost = market.buy_asset(asset, row)
                size = self.get_bet_size(account)
                shares = size / price
                if shares > self.min_shares_allowed:
                    portfolio.update(asset=asset, shares=shares, position='Long')
                    account.update(size, typ='debit')
                    value = account.cash_at_hand + portfolio.shares[asset] * price
                    return dict(shares=shares, price=price, action='Long')
                else:
                    return dict(shares=0., price=row['close'], action='StayOut')

            elif portfolio.positions[asset][-1] == 'Long':
                return dict(shares=portfolio.shares.get(asset, 0), price=row['close'], action='Hold')

            elif portfolio.positions[asset][-1] == 'Short':
                price, trade_cost = market.buy_asset(row)
                shares = -1 * portfolio.shares[asset]
                size = shares * price
                account.update(size, typ='debit')
                portfolio.update(asset=asset,
                                 shares=shares,
                                 position='OOM')
                return dict(shares=shares, price=price, action='Long')

        elif row['signal'] == 'strategy':
            # print('Sell')
            if portfolio.positions[asset][-1] == 'OOM':
                # ToDo: implement short
                return dict(shares=0, price=row['close'], action='StayOut')

            elif portfolio.positions[asset][-1] == 'Long':
                price, trade_cost = market.sell_asset(asset, row)
                shares = portfolio.shares[asset]
                size = shares * price
                account.update(size, typ='credit')
                portfolio.update(asset=asset, shares=-shares, position='OOM')
                value = account.cash_at_hand
                return dict(shares=-shares, price=price, action='Sell')
            elif portfolio.positions[asset][-1] == 'Short':
                # ToDo: implement short
                return dict(shares=0, price=row['close'], action='StayOut')
        elif row['signal'] == 'h':
            # print('Hold')
            return dict(shares=portfolio.shares.get(asset, 0), price=row['close'], action='Hold')
        else:
            # print('Nothing')
            return dict(shares=0, price=row['close'], action='StayOut')

    def get_bet_size(self, account: Account,
                     confidence: float = 1.,
                     position_type: str = 'Long'):
        if position_type == 'Long':
            sizing_function = lambda x: self.max_bet_size * (1 - np.exp(-3 * x))
            size = sizing_function(confidence)
            return size * account.cash_at_hand
        else:
            # ToDo: Implement position sizing for going short
            pass


class StrategyRunner:

    def __init__(self, df: pd.DataFrame,
                 strategy: StrategyFactory = None,
                 account: Account = None,
                 portfolio: Portfolio = None,
                 simulator: MarketSimulator = None):
        self.strategy = strategy
        self.account = account
        self.portfolio = portfolio
        self.market_simulator = simulator
        self.reset()

    def reset(self):
        self.history = dict(time=[], price=[],
                            shares=[], action=[],
                            asset=[], account_value=[])

    def update_history(self, **kwargs):

        for k, v in self.history.items():
            v.append(kwargs.get(k, np.NaN))

    def run(self, reset: bool = True):

        if reset:
            self.reset()
        try:
            for timestamp, row in self.market_simulator:
                # print(timestamp)
                results = self.strategy.execute_current_timestamp(row=row,
                                                                  timestamp=timestamp,
                                                                  account=self.account,
                                                                  portfolio=self.portfolio,
                                                                  market=self.market_simulator)
                results['time'] = timestamp
                results['asset'] = row['asset']
                results['account_value'] = self.account.cash_at_hand + row['close'] * self.portfolio.shares.get(
                    results['asset'], 0)
                self.update_history(**results)
        except StopIteration:
            print("Simulation ended")

        self.history = pd.DataFrame(self.history)
        self.history = self.history.set_index('time')


class HodlerStrategy(StrategyFactory):

    def __init__(self, buy_time):
        self.buy_time = buy_time

    def run_algo(self, row: pd.DataFrame,
                 timestamp: Union[pd.Timestamp, datetime],
                 account: Account,
                 portfolio: Portfolio, **kwargs):
        if timestamp == self.buy_time:
            price = row['close']
            shares = account.cash_at_hand / price
            size = account.cash_at_hand
            account.update(size, typ='debit')
            portfolio.update(asset=row['asset'],
                             shares=shares,
                             position='Long')
            value = account.cash_at_hand + shares * price
            return dict(shares=shares,
                        price=price,
                        action='Long')
        else:
            shares = portfolio.shares[row['asset']]
            price = row['close']
            value = account.cash_at_hand + shares * price
            return dict(shares=shares,
                        price=price,
                        action='Hold')