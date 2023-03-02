import pandas as pd
from math import ceil
import numpy as np
from typing import Tuple, List, Optional



def create_x_y_data_sequence(
        df, 
        seq_length,
        x_columns:Optional[List[str]]=...,
        y_columns:Optional[List[str]]=...
    ) -> Tuple[np.ndarray, np.ndarray]:

    """
    Creates sequences [0:-1] of X data and end of seqence [-1] as Y data.

    seqlength defines the window over which to split the data,
    here X is [0:seq_length-1] and Y is equal to sequence[seq_length]

    Returns two pandas DataFrames, corresponding to x and y.
    """

    num_rows = ceil(len(df)/seq_length)

    temp_df = df if x_columns == ... else df[x_columns]
    temp_x_arr = temp_df.to_numpy().copy()

    temp_df = df if y_columns == ... else df[y_columns]
    temp_y_arr = temp_df.to_numpy().copy()

    if isinstance(df, pd.DataFrame):
        x_len = len(x_columns if x_columns != ... else df.columns)
        y_len = len(y_columns if y_columns != ... else df.columns)
    elif isinstance(df, pd.Series):
        x_len, y_len = 1, 1


    temp_x_arr.resize((num_rows, seq_length, x_len))
    temp_y_arr.resize((num_rows, seq_length, y_len))
    

    x = temp_x_arr[:,0:seq_length-1,:]
    y = temp_y_arr[:,-1,:]
        
    return x, y