"""Group of functions to work with pandas DataFrames.
Can be move to a separate package so it can be used in all projects.

Currently mainly taken from the following sources on PyPI:
- pimms-learn
- njab
"""

from importlib import metadata

__version__ = metadata.version("dsp_pandas")

from . import format as pd_format

# The __all__ variable is a list of variables which are imported
# when a user does "from example import *"
__all__ = ["pd_format"]

pd_format.set_pandas_number_formatting()
