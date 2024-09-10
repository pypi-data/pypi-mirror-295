"""Helper to read and write data from and to different formats."""

from pathlib import Path
from types import SimpleNamespace

import pandas as pd


def read_all_excel_sheets(
    fname: str | Path, index_col: int = 0, drop_empty: bool = True
) -> SimpleNamespace:
    """Import all sheets as pandas DataFrames from an Excel table into a SimpleNamespace object.

    Parameters
    ----------
    fname : str | Path
        Path to the Excel file.
    index_col : int, optional
        Index columns to use, by default 0
    drop_empty : bool, optional
        Wheater to drop the entirely missing columns although they might be named, by default True

    Returns
    -------
    SimpleNamespace
        Object with all the sheet names as attributes. White space are replaced by underscores.
    """
    with pd.ExcelFile(fname) as excel_reader:
        # Get the sheet names
        sheet_names = excel_reader.sheet_names
        sheets = SimpleNamespace(sheet_names=sheet_names)

        for sheet_name in sheet_names:
            _df = excel_reader.parse(sheet_name, index_col=index_col)
            if drop_empty:
                _df = _df.dropna(axis=1, how="all").dropna(axis=0, how="all")
            sheet_name = sheet_name.replace(" ", "_")
            setattr(sheets, sheet_name, _df)
    return sheets
