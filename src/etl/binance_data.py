from binance import Client
import pandas as pd
from math import ceil

def get_client(api_key:str=None, api_secret:str=None):
    return Client(
        api_key=api_key,
        api_secret=api_secret
    )

def get_klines(
        client,
        symbol:str="BTCUSDT",
        interval:str="1h",
        limit:int=100,
        startTime:int=None,
        endTime:int=None,
    ) -> pd.DataFrame:
    columns = [
        "kline_open_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "kline_close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore"
    ]

    num_calls = ceil(limit/1000)

    try:
        for call in range(1, num_calls+1):
            
            n_limit = limit if limit < 1000 else 1000
            
            if call == 1:
                df = pd.DataFrame(
                    client.get_klines(
                        symbol=symbol,
                        interval=interval,
                        limit=n_limit,
                        startTime=startTime,
                        endTime=endTime
                    ),
                    columns=columns
                )
            else:
                temp_df = pd.DataFrame(
                    client.get_klines(
                        symbol=symbol,
                        interval=interval,
                        limit=n_limit,
                        startTime=startTime,
                        endTime=endTime,
                    ),
                    columns=columns
                )

                df = pd.concat([df, temp_df])
            

            startTime = df["kline_open_time"].max() + 1
            
            limit -= n_limit
    except Exception as e:
        print(e)
    
    finally:
        for column in df.columns:
            df[column] = pd.to_numeric(df[column])
        
        return df
    
def create_change(
        df:pd.DataFrame, 
        columns:list[str], 
        lead_size:int=1
    ):
    lag_columns = []
    for column in columns:
        lag_columns.append(f"{column}_change") 
    
    df[lag_columns] = df[columns].shift(lead_size)

    for column, new_column in zip(columns, lag_columns):
        df[new_column] = df[column] / df[new_column]

    return df