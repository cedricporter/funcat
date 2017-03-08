#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#


import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()

version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

__main_version__ = "%s.%s.x" % (version_info[0], version_info[1])

del pkgutil


from .time_series import PriceSeries
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
)
from .context import (
    ExecutionContext as funcat_execution_context,
    symbol,
    set_current_stock,
    set_current_date,
    set_data_backend,
)
from .helper import select
from .data.tushare_backend import TushareDataBackend


# close: CLOSE, C, c
for name in ["open", "high", "low", "close", "volume"]:
    cls = type("{}Series".format(name.capitalize()), (PriceSeries, ), {"name": name})
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

S = set_current_stock
T = set_current_date

funcat_execution_context(date=20170104,
                         stock="000001.XSHG",
                         data_backend=TushareDataBackend())._push()
