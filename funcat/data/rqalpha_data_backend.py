# -*- coding: utf-8 -*-
#

import copy
import os
import datetime

import numpy as np
from numpy.lib import recfunctions as rfn

from .backend import DataBackend
from ..utils import get_date_from_int, get_int_date


class RQAlphaDataBackend(DataBackend):
    """
    目前仅支持日数据
    """
    skip_suspended = True

    def __init__(self, bundle_path="~/.rqalpha/bundle"):
        try:
            import rqalpha
        except ImportError:
            print("-" * 50)
            print("Run `pip install rqalpha` to install rqalpha first")
            print("-" * 50)
            raise

        # # FIXME
        # import warnings
        # warnings.simplefilter(action="ignore", category=FutureWarning)

        from rqalpha.data.base_data_source import BaseDataSource
        from rqalpha.data.data_proxy import DataProxy

        self.data_proxy = DataProxy(BaseDataSource(os.path.expanduser(bundle_path)))

    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        assert freq == "1d"

        start = get_date_from_int(start)
        end = get_date_from_int(end)

        bar_count = (end - start).days

        bars = self.data_proxy.history_bars(
            order_book_id, bar_count, freq, field=None,
            dt=datetime.datetime.combine(end, datetime.time(23, 59, 59)))

        if bars is None or len(bars) == 0:
            raise KeyError("empty bars {}".format(order_book_id))
        bars = bars.copy()

        return bars

    def get_order_book_id_list(self):
        """获取所有的
        """
        import pandas as pd
        insts = self.data_proxy.all_instruments("CS")
        if isinstance(insts, pd.DataFrame):
            # for old version of RQAlpha
            return sorted(insts.order_book_id.tolist())
        else:
            # for new version fo RQAlpha
            return sorted([inst.order_book_id for inst in insts])

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
