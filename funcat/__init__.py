#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from .time_series import PriceSeries
from .func import SumSeries, MovingAverageSeries, CrossOver, minimum, maximum, every, count, hhv, llv, Ref, iif
from .context import ExecutionContext, symbol, set_current_stock as S, set_current_date as T, set_data_backend
from .helper import select
from .data.tushare_backend import TushareDataBackend


# close: CLOSE, C, c
for name in ["open", "high", "low", "close", "volume"]:
    cls = type("{}Series".format(name.capitalize()), (PriceSeries, ), {"name": name})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj


ma = MA = MovingAverageSeries
sum = SUM = SumSeries
cross = CROSS = CrossOver
ref = REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv
IF = IIF = iif

ExecutionContext(date=20170104,
                 stock="000001.XSHG",
                 data_backend=TushareDataBackend())._push()
