import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

DEFAULT_TIMEFRAME = mt5.TIMEFRAME_D1

def initialize(server: str, login: int, password: str, path: str):
    if not mt5.initialize(path, login=login, server=server, password=password,  timeout=300000,):
        raise Exception(f"initialize() failed, error code {mt5.last_error()}")
    
    # terminal_info = mt5.terminal_info()._asdict()
    # terminal_info_df = pd.DataFrame(list(terminal_info.items()),
    #                             columns=['Property','Value'])
    # print(terminal_info_df)

def get_rates(
        symbol: str,
        date_start = datetime(2013,10,1), 
        date_end = datetime.now(),
        timeframe = DEFAULT_TIMEFRAME
    ) -> pd.DataFrame:
    return mt5.copy_rates_range(symbol, timeframe, date_start,date_end)
    