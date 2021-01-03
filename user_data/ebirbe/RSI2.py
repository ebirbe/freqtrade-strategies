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

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # EMAs
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # RSI2
        dataframe['rsi2'] = ta.RSI(dataframe, timeperiod=2)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Must be oversold on a running uptrend
                (dataframe['close'] > dataframe['ema200']) &
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
