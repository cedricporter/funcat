#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from __future__ import division

import numpy as np

from .utils import wrap_formula_exc, FormulaException
from .context import ExecutionContext


def get_bars():
    data_backend = ExecutionContext.get_data_backend()
    current_date = ExecutionContext.get_current_date()
    stock = ExecutionContext.get_current_stock()
    start_date = data_backend.get_start_date()

    try:
        bars = data_backend.get_price(stock, start=start_date, end=current_date)
    except KeyError:
        return np.array([])

    # return empty array direct
    if len(bars) == 0:
        return bars

    # if stock is suspend, just skip
    if data_backend.skip_suspended and bars["date"][-1] != current_date:
        return np.array([])

    return bars


def fit_series(s1, s2):
    size = min(len(s1), len(s2))
    if size == 0:
        raise FormulaException("series size == 0")
    s1, s2 = s1[-size:], s2[-size:]
    return s1, s2


def get_value(val):
    if isinstance(val, TimeSeries):
        return val.value
    else:
        return val


def get_series(val):
    if isinstance(val, TimeSeries):
        return val.series
    else:
        return DuplicateNumericSeries(val).series


class TimeSeries(object):
    '''
    https://docs.python.org/3/library/operator.html
    '''

    @property
    def series(self):
        raise NotImplementedError

    @property
    @wrap_formula_exc
    def value(self):
        return self.series[-1]

    def __len__(self):
        return len(self.series)

    @wrap_formula_exc
    def __lt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 < s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __gt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 > s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __eq__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 == s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __ge__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 >= s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __le__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 <= s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __sub__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 - s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __add__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 + s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __mul__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 * s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __truediv__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        series = s1 / s2
        return NumericSeries(series)

    __div__ = __truediv__

    def __bool__(self):
        return len(self) > 0 and bool(self.value)

    def __and__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        return BoolSeries(s1 & s2)

    def __or__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        return BoolSeries(s1 | s2)

    # fix bug in python 2
    __nonzero__ = __bool__

    def __repr__(self):
        return str(self.value)


class NumericSeries(TimeSeries):
    def __init__(self, series=[]):
        super(NumericSeries, self).__init__()
        self._series = series
        self.extra_create_kwargs = {}

    @property
    def series(self):
        return self._series

    def __getitem__(self, index):
        assert isinstance(index, int) and index >= 0
        return self.__class__(self.series[:len(self.series) - index], **self.extra_create_kwargs)


class DuplicateNumericSeries(NumericSeries):
    def __init__(self, val):
        super(DuplicateNumericSeries, self).__init__(np.full(5000, val, dtype=np.float64))


class PriceSeries(NumericSeries):
    def __init__(self, series=None, dynamic_update=False):
        super(PriceSeries, self).__init__(series)
        self._dynamic_update = dynamic_update

    def _ensure_series_update(self):
        if self._dynamic_update:
            # TODO: cache
            bars = get_bars()
            if len(bars) > 0:
                self._series = bars[self.name]
            else:
                self._series = bars

    @property
    def series(self):
        self._ensure_series_update()
        return super(PriceSeries, self).series

    @property
    def name(self):
        raise NotImplementedError


class BoolSeries(NumericSeries):
    pass
