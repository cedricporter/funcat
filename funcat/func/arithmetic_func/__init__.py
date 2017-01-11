#!/usr/bin/env python
# encoding: utf-8

import numpy as np

from ...utils import FormulaException
from ...time_series import NumericSeries


def MAX(s1, s2):
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("maximum size == 0")
    s = np.maximum(s1.series, s2.series)
    return NumericSeries(s)


def MIN(s1, s2):
    if len(s1) == 0 or len(s2) == 0:
        raise FormulaException("minimum size == 0")
    s = np.minimum(s1.series, s2.series)
    return NumericSeries(s)
