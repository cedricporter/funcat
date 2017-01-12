#!/usr/bin/env python
# encoding: utf-8

import talib

from ...time_series import PriceSeries, get_bars


class TrueRangeSeries(PriceSeries):
    def _ensure_series_update(self):
        if self._dynamic_update:
            bars = get_bars()
            if len(bars) > 0:
                self._series = talib.TRANGE(bars['high'], bars['low'], bars['close'])
            else:
                self._series = bars

    @property
    def name(self):
        return "true_range"


OpenSeries = type("OpenSeries", (PriceSeries, ), {"name": "open"})
HighSeries = type("HighSeries", (PriceSeries, ), {"name": "high"})
LowSeries = type("LowSeries", (PriceSeries, ), {"name": "low"})
CloseSeries = type("CloseSeries", (PriceSeries, ), {"name": "close"})
VolumeSeries = type("VolumeSeries", (PriceSeries, ), {"name": "volume"})

OPEN = O = OpenSeries(dynamic_update=True)
HIGH = H = HighSeries(dynamic_update=True)
LOW = L = LowSeries(dynamic_update=True)
CLOSE = C = CloseSeries(dynamic_update=True)
VOLUME = V = VolumeSeries(dynamic_update=True)
TR = TrueRangeSeries(dynamic_update=True)

