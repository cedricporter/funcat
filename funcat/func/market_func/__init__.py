#!/usr/bin/env python
# encoding: utf-8

from ...time_series import PriceSeries


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
