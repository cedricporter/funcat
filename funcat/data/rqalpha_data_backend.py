#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#
import copy
import os
import datetime

import numpy as np

from .backend import DataBackend
from ..utils import get_date_from_int, get_int_date


class RQAlphaDataBackend(DataBackend):
    """
    目前仅支持日数据
    """
    skip_suspended = False

    def __init__(self, bundle_path="~/.rqalpha/bundle", start_date="2010-01-01"):
        try:
            import rqalpha
        except ImportError:
            print("-" * 50)
            print("Run `pip install rqalpha` to install rqalpha first")
            print("-" * 50)
            raise

        # FIXME
        import warnings
        warnings.simplefilter(action="ignore", category=FutureWarning)

        from rqalpha.data.base_data_source import BaseDataSource
        from rqalpha.data.data_proxy import DataProxy

        self.analyse_start_date = start_date
        self.data_proxy = DataProxy(BaseDataSource(os.path.expanduser(bundle_path)))

    def get_price(self, order_book_id, start, end):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_date_from_int(start)
        end = get_date_from_int(end)

        bar_count = (end - start).days
        bars = self.data_proxy.history_bars(
            order_book_id, bar_count, "1d", field=None,
            dt=datetime.datetime.combine(end, datetime.time(23, 59, 59)))
        if bars is None or len(bars) == 0:
            raise KeyError("empty bars {}".format(order_book_id))
        bars = bars.copy()
        origin_bars = bars = bars.astype([
            ('datetime', '<u8'), ('open', '<f8'), ('close', '<f8'),
            ('high', '<f8'), ('low', '<f8'), ('volume', '<f8'), ('total_turnover', '<f8')])

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
        return sorted(self.data_proxy.all_instruments("CS").order_book_id.tolist())

    def get_start_date(self):
        """获取回溯开始时间
        """
        return str(self.analyse_start_date)

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        return self.data_proxy.instruments(order_book_id).symbol

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        start = get_date_from_int(start)
        end = get_date_from_int(end)
        trading_dates = self.data_proxy.get_trading_dates(start, end).tolist()
        trading_dates = [get_int_date(dt.date()) for dt in trading_dates]
        return trading_dates
