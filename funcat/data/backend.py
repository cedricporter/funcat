#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#


class DataBackend(object):
    skip_suspended = True

    def get_price(self, order_book_id, start, end):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        raise NotImplementedError

    def get_order_book_id_list(self):
        """获取所有的
        """
        raise NotImplementedError

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        raise NotImplementedError

    def get_start_date(self):
        """获取回溯开始时间
        """
        raise NotImplementedError

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        raise NotImplementedError
