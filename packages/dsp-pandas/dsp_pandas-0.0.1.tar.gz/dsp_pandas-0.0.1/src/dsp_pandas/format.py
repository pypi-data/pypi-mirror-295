"""Format pandas display options for better readability."""

import pandas as pd
import pandas.io.formats.format as pf


def set_pandas_options(
    max_columns: int = 100,
    max_row: int = 30,
    min_row: int = 20,
    float_format: str = "{:,.3f}",
) -> None:
    """Update default pandas options for better display."""
    pd.options.display.max_columns = max_columns
    pd.options.display.max_rows = max_row
    pd.options.display.min_rows = min_row
    set_pandas_number_formatting(float_format=float_format)


def set_pandas_number_formatting(float_format="{:,.3f}") -> None:
    """Format large numbers with commas and decimals."""
    pd.options.display.float_format = float_format.format
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/
    # pandas.describe_option.html#pandas.describe_option
    pd.options.styler.format.thousands = ","
    # # https://github.com/pandas-dev/pandas/blob/main/pandas/io/formats/format.py#L1475
    # Originally found: https://stackoverflow.com/a/29663750/9684872

    try:
        # latest pandas verions
        base_class = pf.GenericArrayFormatter
    except AttributeError:
        # older pandas versions
        base_class = pf._GenericArrayFormatter

    class IntArrayFormatter(base_class):

        def _format_strings(self):
            formatter = self.formatter or "{:,d}".format
            fmt_values = [formatter(x) for x in self.values]
            return fmt_values

    try:
        pf.IntArrayFormatter
        pf.IntArrayFormatter = IntArrayFormatter
    except AttributeError:
        pf._IntArrayFormatter = IntArrayFormatter
