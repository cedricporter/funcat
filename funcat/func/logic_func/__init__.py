#!/usr/bin/env python
# encoding: utf-8

from ...time_series import BoolSeries, fit_series
from ..ref_func import COUNT


def CROSS(s1, s2):
    """s1金叉s2
    :param s1:
    :param s2:
    :returns: bool序列
    :rtype: BoolSeries
    """
    series1, series2 = fit_series(s1.series, s2.series)
    cond1 = series1 > series2
    series1, series2 = fit_series(s1[1].series, s2[1].series)
    cond2 = series1 <= series2  # s1[1].series <= s2[1].series
    cond1, cond2 = fit_series(cond1, cond2)
    s = cond1 & cond2
    return BoolSeries(s)


def every(cond, n):
    return COUNT(cond, n) == n
