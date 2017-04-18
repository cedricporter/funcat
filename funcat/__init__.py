# -*- coding: utf-8 -*-
#

import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()

version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

__main_version__ = "%s.%s.x" % (version_info[0], version_info[1])

del pkgutil

import numpy as np

from .time_series import MarketDataSeries
from .func import (
    SumSeries,
    AbsSeries,
    MovingAverageSeries,
    WeightedMovingAverageSeries,
    ExponentialMovingAverageSeries,
    CrossOver,
    minimum,
    maximum,
    every,
    count,
    hhv,
    llv,
    Ref,
    iif,
    MACDSeries,
)
from .context import (
    ExecutionContext as funcat_execution_context,
    symbol,
    set_current_security,
    set_current_date,
    set_start_date,
    set_data_backend,
    set_current_freq,
)
from .helper import select
from .data.tushare_backend import TushareDataBackend


# close: CLOSE, C, c
for name in ["open", "high", "low", "close", "volume", "datetime"]:
    dtype = np.float64 if name != "datetime" else np.uint64
    cls = type("{}Series".format(name.capitalize()), (MarketDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj


MA = MovingAverageSeries
WMA = WeightedMovingAverageSeries
EMA = ExponentialMovingAverageSeries

SUM = SumSeries
ABS = AbsSeries

CROSS = CrossOver
REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv
IF = IIF = iif

S = set_current_security
T = set_current_date

MACD = MACDSeries(dynamic_update=True)

funcat_execution_context(date=20170104,
                         order_book_id="000001.XSHG",
                         data_backend=TushareDataBackend())._push()
