from sqlalchemy import create_engine, text
import pandas as pd

def get_engine():
    return create_engine("sqlite:///../binance_data.sqlite")

def get_latest_kline(
        table_name:str,
        column:str="kline_open_time"
    ):
    engine = get_engine()

    with engine.connect() as conn:
        stmt = text(f"select {column} from {table_name} order by {column} desc limit 1;")

        latest_kline = conn.execute(stmt).fetchone()[0]

        return latest_kline
    

def sql_to_df(table_name:str, chunksize:int=None):

    engine = get_engine()
    
    with engine.connect() as conn:
        df = pd.read_sql_table(
            table_name, 
            conn, 
            chunksize=chunksize
        )
    
    return df