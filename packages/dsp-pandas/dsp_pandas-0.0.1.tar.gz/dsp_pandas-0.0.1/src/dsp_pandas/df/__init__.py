"""Helpers to identify interesting data in a pandas DataFrame."""

from types import SimpleNamespace

import pandas as pd

__all__ = ["get_unique_non_unique_columns"]


def unique_cols(s: pd.Series) -> bool:
    """Check all entries are equal in pandas.Series

    Ref: https://stackoverflow.com/a/54405767/968487

    Parameters
    ----------
    s : pandas.Series
        Series to check uniqueness

    Returns
    -------
    bool
        Boolean on if all values are equal.
    """
    return (s.iloc[0] == s).all()


def get_unique_non_unique_columns(df: pd.DataFrame) -> SimpleNamespace:
    """Get back a namespace with an column.Index both
    of the unique and non-unique columns.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to check for unique columns.

    Returns
    -------
    types.SimpleNamespace
        SimpleNamespace with `unique` and `non_unique` column names indices.
    """

    mask_unique_columns = df.apply(unique_cols)

    columns = SimpleNamespace()
    columns.unique = df.columns[mask_unique_columns]
    columns.non_unique = df.columns[~mask_unique_columns]
    return columns


def combine_value_counts(X: pd.DataFrame, dropna=True) -> pd.DataFrame:
    """Pass a selection of columns to combine it's value counts.

    This performs no checks. Make sure the scale of the variables
    you pass is comparable.

    Parameters
    ----------
    X : pandas.DataFrame
        A DataFrame of several columns with values in a similar range.
    dropna : bool, optional
        Exclude NA values from counting, by default True

    Returns
    -------
    pandas.DataFrame
        DataFrame of combined value counts.
    """
    freq_targets = list()
    for col in X.columns:
        freq_targets.append(X[col].value_counts(dropna=dropna).rename(col))
    freq_targets = pd.concat(freq_targets, axis=1, sort=True)
    return freq_targets
