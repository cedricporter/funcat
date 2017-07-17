# -*- coding: utf-8 -*-
#

from __future__ import division

import six
import numpy as np

from .utils import wrap_formula_exc, FormulaException
from .context import ExecutionContext


def get_bars(freq):
    data_backend = ExecutionContext.get_data_backend()
    current_date = ExecutionContext.get_current_date()
    order_book_id = ExecutionContext.get_current_security()
    start_date = ExecutionContext.get_start_date()

    try:
        bars = data_backend.get_price(order_book_id, start=start_date, end=current_date, freq=freq)
    except KeyError:
        return np.array([])

    # return empty array direct
    if len(bars) == 0:
        return bars

    # if security is suspend, just skip
    if data_backend.skip_suspended and bars["datetime"][-1] // 1000000 != current_date and freq not in ("W", "M"):
        return np.array([])

    return bars


def fit_series(*series_list):
    size = min(len(series) for series in series_list)
    if size == 0:
        raise FormulaException("series size == 0")
    new_series_list = [series[-size:] for series in series_list]
    return new_series_list


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


def ensure_timeseries(series):
    if isinstance(series, TimeSeries):
        return series
    else:
        return DuplicateNumericSeries(series)


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
        try:
            return self.series[-1]
        except IndexError:
            raise FormulaException("DATA UNAVAILABLE")

    def __len__(self):
        return len(self.series)

    @wrap_formula_exc
    def __lt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 < s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __gt__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 > s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __eq__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 == s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __ne__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 != s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __ge__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 >= s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __le__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 <= s2
        return BoolSeries(series)

    @wrap_formula_exc
    def __sub__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 - s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __rsub__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 - s1
        return NumericSeries(series)

    @wrap_formula_exc
    def __add__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 + s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __radd__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 + s1
        return NumericSeries(series)

    @wrap_formula_exc
    def __mul__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 * s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __rmul__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 * s1
        return NumericSeries(series)

    @wrap_formula_exc
    def __truediv__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s1 / s2
        return NumericSeries(series)

    @wrap_formula_exc
    def __rtruediv__(self, other):
        s1, s2 = fit_series(self.series, get_series(other))
        with np.errstate(invalid='ignore'):
            series = s2 / s1
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

    @wrap_formula_exc
    def __invert__(self):
        with np.errstate(invalid='ignore'):
            series = ~self.series
        return BoolSeries(series)

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
        return self.__class__(series=self.series[:len(self.series) - index], **self.extra_create_kwargs)


class DuplicateNumericSeries(NumericSeries):
    # FIXME size should come from other series
    def __init__(self, series, size=640000):
        try:
            val = series[-1]
        except:
            val = series
        super(DuplicateNumericSeries, self).__init__(np.full(size, val, dtype=np.float64))


class MarketDataSeries(NumericSeries):
    """MarketDataSeries

    MarketDataSeries 与其他 TimeSeries 最大的区别是，
    其值是通过动态根据当前时间和当前关注的标的更新
    """
    def __init__(self, series=None, dynamic_update=False, freq=None):
        super(MarketDataSeries, self).__init__(series)
        self._dynamic_update = dynamic_update
        self._freq = freq

    def _ensure_series_update(self):
        if self._dynamic_update:
            # TODO: cache
            freq = self._freq if self._freq is not None else ExecutionContext.get_current_freq()
            bars = get_bars(freq)
            if len(bars) > 0:
                self._series = bars[self.name].astype(self.dtype)
            else:
                self._series = bars

    def __getitem__(self, index):
        if isinstance(index, int):
            assert index >= 0

        if isinstance(index, six.string_types):
            unit = index[-1]
            period = int(index[:-1])
            assert unit in ["m", "d"]
            assert period > 0
            freq = index
            # 因为是行情数据，所以需要动态更新
            time_series = self.__class__(dynamic_update=True, freq=freq, **self.extra_create_kwargs)
            return time_series

        return self.__class__(series=self.series[:len(self.series) - index], **self.extra_create_kwargs)

    @property
    def series(self):
        self._ensure_series_update()
        return super(MarketDataSeries, self).series

    @property
    def dtype(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError


class BoolSeries(NumericSeries):
    pass
