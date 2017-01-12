#!/usr/bin/env python
# encoding: utf-8

import numpy as np

from ..market_func import TR
from ...utils import FormulaException
from ...time_series import NumericSeries, get_talib_series


def COUNT(cond, n):
    # TODO lazy compute
    series = cond.series
    size = len(cond.series) - n
    try:
        result = np.full(size, 0, dtype=np.int)
    except ValueError as e:
        raise FormulaException(e)
    for i in range(size - 1, 0, -1):
        s = series[-n:]
        result[i] = len(s[s == True])
        series = series[:-1]
    return NumericSeries(result)


def HHV(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        result = np.full(size, 0, dtype=np.float64)
    except ValueError as e:
        raise FormulaException(e)
    for i in range(size - 1, 0, -1):
        s = series[-n:]
        result[i] = s.max()
        series = series[:-1]
    return NumericSeries(result)


def LLV(s, n):
    # TODO lazy compute
    series = s.series
    size = len(s.series) - n
    try:
        result = np.full(size, 0, dtype=np.float64)
    except ValueError as e:
        raise FormulaException(e)
    for i in range(size - 1, 0, -1):
        s = series[-n:]
        result[i] = s.min()
        series = series[:-1]
    return NumericSeries(result)


def REF(s1, n):
    return s1[n]


def SUM(series, period):
    if isinstance(series, NumericSeries):
        series = series.series
        series[series == np.inf] = 0
        series[series == -np.inf] = 0
    series = get_talib_series(series, period, name="SUM")
    series.extra_create_kwargs["period"] = period
    return series


def SMA(series, period, weight):
    """ 简单移动平均线
    SMA(X,N,P):SMA=(P*X+(N-P)*SMA[i-1])/N
    """
    if isinstance(series, NumericSeries):
        series = series.series
    series = get_talib_series(series, period, name="SMA")
    series.extra_create_kwargs["period"] = period


def MA(series, period):
    """ 移动平均线
    MA(X,N)=(X1+X2+X3+...+Xn)/N
    """
    if isinstance(series, NumericSeries):
        series = series.series
    series = get_talib_series(series, period, name="MA")
    series.extra_create_kwargs["period"] = period
    return series


def EMA(series, period):
    """ 指数移动平均线
    EMA(X,N),EXPMA(X,N):EMA=(2*X+(N-1)*EMA[i-1])/(N+1)
    """
    if isinstance(series, NumericSeries):
        series = series.series
    series = get_talib_series(series, period, name="EMA")
    series.extra_create_kwargs["period"] = period
    return series

EXPMA = EMA


def ATR(period):
    return MA(TR, period)