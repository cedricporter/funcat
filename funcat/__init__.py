#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from .time_series import PriceSeries
from .func import *
from .context import ExecutionContext, symbol, set_current_stock as S, set_current_date as T, set_data_backend
from .helper import select
from .data.tushare_backend import TushareDataBackend


ExecutionContext(date=20170104,
                 stock="000001.XSHG",
                 data_backend=TushareDataBackend())._push()
