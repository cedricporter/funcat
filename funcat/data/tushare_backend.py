#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from .backend import DataBackend
from ..utils import lru_cache, get_str_date_from_int, get_int_date


class TushareDataBackend(DataBackend):
    def __init__(self, start_date="2011-01-01"):
        import tushare as ts
        self.start_date = start_date
        self.ts = ts
        self.stock_basics = self.ts.get_stock_basics()
        self.code_name_map = self.stock_basics[["name"]].to_dict()["name"]

    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        is_index = False
        if ((order_book_id.startswith("0") and order_book_id.endswith(".XSHG")) or
            (order_book_id.startswith("3") and order_book_id.endswith(".XSHE"))
            ):
            is_index = True
        df = self.ts.get_k_data(code, start=start, end=end, index=is_index)
        df["date"] = df["date"].apply(lambda x: int(x.replace("-", "")))
        df = df.set_index("date")
        del df["code"]
        arr = df.to_records()
        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        info = self.ts.get_stock_basics()
        code_list = info.index.sort_values().tolist()
        order_book_id_list = [
            (code + ".XSHG" if code.startswith("6") else code + ".XSHE")
            for code in code_list
        ]
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        df = self.ts.get_k_data("000001", index=True, start=start, end=end)
        trading_dates = [get_int_date(date) for date in df.date.tolist()]
        return trading_dates

    @lru_cache()
    def get_start_date(self):
        """获取回溯开始时间
        """
        return self.start_date

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        code = self.convert_code(order_book_id)
        return "{}[{}]".format(order_book_id, self.code_name_map.get(code))
