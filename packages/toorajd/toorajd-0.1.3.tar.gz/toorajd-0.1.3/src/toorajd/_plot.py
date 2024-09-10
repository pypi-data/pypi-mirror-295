import os
import polars as pl
import pandas as pd
from typing import Union


class Plot:
    """Base class for all Mirshahi Plots
    :param data: the data that will be used for plotting. Can be a path or polars/pandas dataframe.
    :param sep: the field delimeter for the data if it is a file that will be read. Will automatically read parquet files. Default = ' '.
    :param **kwargs: any additional keywords to be passed to pl.read_csv()
    """

    def __init__(
        self, data: Union[str, pl.DataFrame, pd.DataFrame], sep: str = " ", **kwargs
    ) -> None:
        self.data = self._load_data(data, sep, kwargs)

    @staticmethod
    def _load_data(data, sep, kwargs):
        if isinstance(data, str):
            if os.path.exists(data):
                if data.endswith(".parquet"):
                    return pl.read_parquet(data, **kwargs)
                elif not data.endswith(".parquet"):
                    return pl.read_csv(data, separator=sep, **kwargs)
                else:
                    raise ValueError(f"File format not supported: {data}")
            else:
                raise FileNotFoundError(
                    f"File not found: {data}. Please check the path and try again."
                )
        elif isinstance(data, pl.DataFrame):
            return data
        elif isinstance(data, pd.DataFrame):
            return pl.DataFrame(data)
        else:
            raise ValueError(
                f"Data type not supported: {type(data)}. Please provide a path or a polars/pandas dataframe."
            )

    def peek(self):
        """Take a peek at the data that will be used for plotting."""
        return self.data.head()

    def plot(self):
        raise NotImplementedError("Method not implemented yet.")
