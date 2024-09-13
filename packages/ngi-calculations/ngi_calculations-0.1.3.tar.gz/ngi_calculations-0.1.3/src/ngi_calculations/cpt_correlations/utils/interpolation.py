from typing import List

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def interpolate_missing_values(df: pd.DataFrame, key_col: str, inplace: bool = False, col_list: List[str] = False):
    # Whether to mutate the provided DataFrame or not
    _df = df if inplace else df.copy()

    # Get the columns where interpolation should be performed (any column with NaN)
    _cols: List[str] = col_list if col_list else _df.columns[df.isna().any()].tolist()

    # Store the key col values as a numpy array
    key_values = np.array(_df[key_col].values.tolist())

    # iterate over the columns that contains NaN
    for col in _cols:
        _values = _df[[key_col, col]].dropna()  # DataFrame of existing values in col

        col_values_finite = np.array(_values[col].values.tolist())  # Array of existing values in col

        key_values_finite = np.array(_values[key_col].values.tolist())  # Array of existing values in col

        if col_values_finite.size > 0:
            # Set-up the interpolation function (it must be done again for each column)
            f = interp1d(key_values_finite, col_values_finite, fill_value="extrapolate")
            # Set the interpolate data
            _df[col] = f(key_values)

    return _df
