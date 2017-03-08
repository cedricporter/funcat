#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#
import copy

import numpy as np

from .backend import DataBackend
from ..utils import get_date_from_int


class RQAlphaBacktestDataBackend(DataBackend):
    """
    目前仅支持日数据
    """
    skip_suspended = False

    def __init__(self):
        from rqalpha.api import (
            history_bars,
            all_instruments,
            instruments,
        )
        from rqalpha.environment import Environment
        from rqalpha.events import Events

        from ..context import set_current_date

        self.set_current_date = set_current_date

        self.history_bars = history_bars
        self.all_instruments = all_instruments
        self.instruments = instruments
        self.rqalpha_env = Environment.get_instance()

        self.rqalpha_env.event_bus.add_listener(Events.PRE_BEFORE_TRADING, self._pre_before_trading)
        self.rqalpha_env.event_bus.add_listener(Events.PRE_BAR, self._pre_handle_bar)

    def _pre_before_trading(self, *args, **kwargs):
        calendar_date = self.rqalpha_env.calendar_dt.date()
        self.set_current_date(calendar_date)

    def _pre_handle_bar(self, *args, **kwargs):
        calendar_date = self.rqalpha_env.calendar_dt.date()
        self.set_current_date(calendar_date)

    def get_price(self, order_book_id, start, end):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        # start = get_date_from_int(start)
        # end = get_date_from_int(end)
        # bar_count = (end - start).days

        # TODO: this is slow, make it run faster
        bar_count = 1000
        origin_bars = bars = self.history_bars(order_book_id, bar_count, "1d")

        dtype = copy.deepcopy(bars.dtype)
        names = list(dtype.names)
        names[0] = "date"
        dtype.names = names
        bars = np.array(bars, dtype=dtype)

        bars["date"] = origin_bars["datetime"] / 1000000

        return bars

    def get_order_book_id_list(self):
        """获取所有的
        """
        return sorted(self.all_instruments("CS").order_book_id.tolist())

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        raise NotImplementedError

    def get_start_date(self):
        """获取回溯开始时间
        """
        return str(self.rqalpha_env.config.base.start_date)

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        return self.instruments(order_book_id).symbol
