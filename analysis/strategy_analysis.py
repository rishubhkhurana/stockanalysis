import numpy as np
from ..strategy.strategy import StrategyRunner

class StrategyAnalyzer:

    def __init__(self, runner: StrategyRunner):
        if not hasattr(runner, 'history'):
            print("Nothing to plot as there is no history")
        self.runner = runner
        self.initialize()

    def initialize(self):
        self.analytics = self.runner.history.copy(deep=True)
        self.analytics['total_size'] = np.abs(self.analytics['price'] * self.analytics['shares'])
        self.statistics = dict()

    def plot(self, **kwargs):
        if not hasattr(self.runner, 'history'):
            print("Nothing to plot as there is no history")
        ax = self.runner.history.account_value.plot(**kwargs)
        return ax

    def add_drawdown(self, **kwargs):
        running_max = self.analytics.account_value.cummax()
        self.analytics['drawdown'] = self.analytics.account_value - running_max
        self.statistics['max_drawdown'] = self.analytics.drawdown.min()

    def compute_hold_periods(self):
        """
        Assuming Long only
        """
        sell_indexes = self.analytics[self.analytics.action == 'Sell'].index
        long_indexes = self.analytics[self.analytics.action == 'Long'].index
        hold_out_periods = sell_indexes - long_indexes
        self.hold_out_periods = np.asarray([period.total_seconds() for period in hold_out_periods])
        self.statistics['min_hold_out_minutes'] = np.min(hold_out_periods) / 60
        self.statistics['min_hold_out_days'] = np.min(hold_out_periods) / (60 * 60 * 24)

    def estimate_activity(self):
        self.activity = dict()
        self.activity['WeeklyLong'] = self.analytics.action.resample('W').agg(lambda x: (x == 'Long').sum())
        self.activity['WeeklySell'] = self.analytics.action.resample('W').agg(lambda x: (x == 'Sell').sum())
        self.activity['WeeklyClosedTrades'] = np.minimum(self.activity['WeeklyLong'], self.activity['WeeklySell'])
        self.activity['WeeklyOpenTrades'] = self.activity['WeeklyLong'] - self.activity['WeeklyClosedTrades']

    def annualize_returns(self, periods_per_year: int = 60 * 60 * 24 * 365):
        start_time = self.analytics.index[0]
        end_time = self.analytics.index[-1]
        total_time = (end_time - start_time).total_seconds()
        cummulative_returns = periods_per_year * (
                    (self.analytics.account_value[-1] / self.analytics.account_value[0]) ** (1 / total_time))
        print(f"cummulative returns: {cummulative_returns}")
        self.statistics['cummulative_returns'] = cummulative_returns
        cummulative_returns = (np.log(self.analytics.account_value[-1] / self.analytics.account_value[0])) * (
                    total_time / periods_per_year)
        print(f"Log cummulative returns: {cummulative_returns}")
        self.statistics['log_cummulative_returns'] = cummulative_returns

    def compute_returns_ratios(self):
        entry_value = self.analytics[self.analytics.action == 'Long']['total_size']
        exit_value = self.analytics[self.analytics.action == 'Sell']['total_size']
        self.per_trade_returns = exit_value.values - entry_value.values
        self.statistics['avg_per_trade_returns'] = np.mean(self.per_trade_returns)
        self.statistics['max_per_trade_returns'] = np.max(self.per_trade_returns)
        self.statistics['min_per_trade_returns'] = np.min(self.per_trade_returns)
        self.statistics['cummulative_return'] = 100 * (
                    self.analytics.account_value.iloc[-1] / self.analytics.account_value.iloc[0] - 1.)
        self.per_time_returns = self.analytics['account_value'].pct_change()
        self.annualize_returns(self.annualize_returns())
        # ToDo: Top 10 and bottom 10 returns summary
        # sharp ratio

