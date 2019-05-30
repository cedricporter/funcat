# -*- coding: utf-8 -*-
import numpy as np

from .time_series import MarketDataSeries
from .func import (
    SumSeries,
    AbsSeries,
    StdSeries,
    SMASeries,
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
    hhvbars,
    llvbars,
    Ref,
    iif,
    ceiling,
    const,
    drawnull,
    zig,
)
from .context import (
    symbol,
    set_current_security,
    set_current_date,
    set_start_date,
    set_data_backend,
    set_current_freq,
)
from .helper import select


# create open high low close volume datetime
for name in ["open", "high", "low", "close", "volume", "datetime"]:
    dtype = np.float64 if name != "datetime" else np.uint64
    cls = type("{}Series".format(name.capitalize()), (MarketDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

VOL = VOLUME

MA = MovingAverageSeries
WMA = WeightedMovingAverageSeries
EMA = ExponentialMovingAverageSeries
SMA = SMASeries

SUM = SumSeries
ABS = AbsSeries
STD = StdSeries

CROSS = CrossOver
REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv
HHVBARS = hhvbars
LLVBARS = llvbars
IF = IIF = iif
CEILING = ceiling
CONST = const
DRAWNULL = drawnull
ZIG = zig  # zig当前以收盘价为准

S = set_current_security
T = set_current_date


__all__ = [
    "OPEN", "O",
    "HIGH", "H",
    "LOW", "L",
    "CLOSE", "C",
    "VOLUME", "V", "VOL",
    "DATETIME",

    "SMA",
    "MA",
    "EMA",
    "WMA",

    "SUM",
    "ABS",
    "STD",

    "CROSS",
    "REF",
    "MAX",
    "MIN",
    "EVERY",
    "COUNT",
    "HHV",
    "LLV",
    "HHVBARS",
    "LLVBARS",
    "IF", "IIF",
    "CEILING",
    "CONST",
    "DRAWNULL",
    "ZIG",

    "S",
    "T",

    "select",
    "symbol",
    "set_current_security",
    "set_current_date",
    "set_start_date",
    "set_data_backend",
    "set_current_freq",
]
