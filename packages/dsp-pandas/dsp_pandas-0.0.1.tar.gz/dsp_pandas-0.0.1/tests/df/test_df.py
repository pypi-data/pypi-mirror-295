import pandas as pd

import dsp_pandas.df


def test_unique_cols():
    s = pd.Series([1, 1, 1, 1, 1])
    assert dsp_pandas.df.unique_cols(s)
    s = pd.Series([1, 1, 1, 1, 2])
    assert not dsp_pandas.df.unique_cols(s)


def test_get_unique_non_unique_columns():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 1], "b": [1, 1, 1, 1, 2]})
    exp = {"unique": ["a"], "non_unique": ["b"]}
    act = dsp_pandas.df.get_unique_non_unique_columns(df).__dict__
    assert act == exp


def test_combine_value_counts():
    df = pd.DataFrame({"a": [1, 2, 2, 2, 3, 3, 3], "b": [1, 1, 1, 2, 2, 3, 3]})
    exp = {"a": {1: 1, 2: 3, 3: 3}, "b": {1: 3, 2: 2, 3: 2}}
    act = dsp_pandas.df.combine_value_counts(df).to_dict()
    assert act == exp
