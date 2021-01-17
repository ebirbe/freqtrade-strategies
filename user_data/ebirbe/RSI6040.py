from datetime import datetime
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy.interface import IStrategy

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class RSI6040(IStrategy):
    """

    author@: Erick Birbe

    """
    minimal_roi = {
        "0": 100,
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.048
    trailing_stop = False
    #trailing_stop_positive = 0.015
    #trailing_stop_positive_offset = 0.016
    #trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '5m'

    order_types = {
        "buy": "market",
        "sell": "market",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = True

    # Candles configurations
    process_only_new_candles = True
    startup_candle_count: int = 20

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                        current_profit: float, **kwargs) -> float:
        if current_profit > 0.01:
            return current_profit - 0.001
        return 1

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # EMAs
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=200)

        # RSI
        dataframe['rsi2'] = ta.RSI(dataframe, timeperiod=2)
        dataframe['rsi14'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi2'], 5)) &
                (dataframe['rsi14'].shift(1) <= 30)
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Selling at the end of an overbought condition
                (qtpylib.crossed_below(dataframe['rsi2'], 95)) &
                (dataframe['rsi14'].shift(1) >= 70)
            ),
            'sell'] = 1
        return dataframe
