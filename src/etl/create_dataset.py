import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from typing import List
from numpy import ndarray


def create_train_test_datasets(
        x:ndarray, 
        y:ndarray,
        create_test_dataset:bool=True,
        test_size:float=0.2
    ) -> tf.data.Dataset:
    
    if create_test_dataset:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        test_dataset = tf.data.Dataset.from_tensor_slices(
            [x_test, y_test]
        )
    
    else:
        test_dataset = tf.convert_to_tensor(())
        x_train, y_train = x, y
    
    train_dataset = tf.data.Dataset.from_tensor_slices(
        [x_train, y_train]
    )

    return train_dataset, test_dataset