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
        "0": 100,
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.03
    trailing_stop = False
    #trailing_stop_positive = 0.005
    #trailing_stop_positive_offset = 0.02
    #trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '15m'

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
    sell_profit_only = False

    # Candles configurations
    process_only_new_candles = True
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # EMAs
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)

        # RSI
        dataframe['rsi2'] = ta.RSI(dataframe, timeperiod=2)
        dataframe['rsi14'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi2'] <= 10) &
                #(qtpylib.crossed_above(dataframe['rsi2'], 10)) &
                (dataframe['rsi14'] >= 35)
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe['close'] >= dataframe['ema20']) &
                    (qtpylib.crossed_below(dataframe['rsi2'], 80)) &
                    (dataframe['rsi14'].shift(1) >= 70)
                )
                | (
                    (dataframe['close'] < dataframe['ema20']) &
                    (qtpylib.crossed_below(dataframe['rsi2'], 80))
                )
                | (
                    (qtpylib.crossed_below(dataframe['close'], dataframe['ema20'])) &
                    (dataframe['rsi14'] < 50)
                )
                #| (qtpylib.crossed_below(dataframe['close'], dataframe['ema20']))
            ),
            'sell'] = 1
        return dataframe
