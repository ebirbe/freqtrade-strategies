# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class RSI2(IStrategy):
    """

    author@: Erick Birbe

    Based on RSI2 Strategy

    """
    minimal_roi = {
        "0": 100
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.03
    trailing_stop = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '1h'

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
    startup_candle_count: int = 100

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # EMAs
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        # RSI2
        dataframe['rsi2'] = ta.RSI(dataframe, timeperiod=2)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Must be oversold on a running uptrend
                (dataframe['close'] > dataframe['ema100']) &
                (dataframe['rsi2'] <= 10)
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Selling at the end of an overbought condition
                (qtpylib.crossed_below(dataframe['rsi2'], 90))
            ),
            'sell'] = 1
        return dataframe
