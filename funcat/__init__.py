#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

import datetime

from .time_series import PriceSeries
from .func import MovingAverageSeries, CrossOver, minimum, maximum, every, count, hhv, llv, Ref
from .context import ExecutionContext, symbol, set_current_stock as S, set_current_date as T, set_data_backend
from .helper import loop


# close: CLOSE, C, c
for name in ["open", "high", "low", "close", "volume"]:
    cls = type("{}Series".format(name.capitalize()), (PriceSeries, ), {"name": name})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj


ma = MA = MovingAverageSeries
cross = CROSS = CrossOver
ref = REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv


ExecutionContext(date=int(datetime.date.today().strftime("%Y%m%d")),
                 stock="000001.XSHG",
                 data_backend=None)._push()
