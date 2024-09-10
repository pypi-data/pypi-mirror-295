import pandas as pd

import dsp_pandas.format


def test_thousands_display():
    dsp_pandas.format.set_pandas_options()
    s = pd.Series([1_000_000])
    assert str(s)[4:13] == "1,000,000"
