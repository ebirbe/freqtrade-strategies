# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MACO(IStrategy):
    """

    author@: Erick Birbe

    EMA Crossover

    """
    minimal_roi = {
        "0": 100
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.2
    #trailing_stop = True
    #trailing_stop_positive = 0.01
    #trailing_stop_positive_offset = 0.02
    #trailing_only_offset_is_reached = True

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
    sell_profit_only = False

    # Candles configurations
    process_only_new_candles = True
    startup_candle_count: int = 100

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # EMAs
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema60'] = ta.EMA(dataframe, timeperiod=60)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                #(dataframe['ema60'] > dataframe['ema100']) &
                #(dataframe['ema20'] > dataframe['ema60']) &
                #(dataframe['close'] > dataframe['ema20']) &
                (qtpylib.crossed_above(dataframe['ema20'], dataframe['ema60']))
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['ema20'], dataframe['ema60']))
            ),
            'sell'] = 1
        return dataframe
