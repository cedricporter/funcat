#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

import datetime

import six

from .utils import get_int_date


class ExecutionContext(object):
    stack = []

    def __init__(self, date=None, stock=None, data_backend=None):
        self._current_date = date
        self._stock = stock
        self._data_backend = data_backend

    def _push(self):
        self.stack.append(self)

    def _pop(self):
        popped = self.stack.pop()
        if popped is not self:
            raise RuntimeError("Popped wrong context")
        return self

    def __enter__(self):
        self._push()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @classmethod
    def get_active(cls):
        return cls.stack[-1]

    @classmethod
    def set_current_date(cls, date):
        """set current simulation date
        :param date: string date, "2016-01-04"
        """
        if isinstance(date, six.string_types):
            date = get_int_date(date)
        elif isinstance(date, datetime.date):
            date = int(date.strftime("%Y%m%d"))
        cls.get_active()._current_date = date

    @classmethod
    def get_current_date(cls):
        return cls.get_active()._current_date

    @classmethod
    def set_current_stock(cls, stock):
        """set current watching stock
        :param stock: "000002.XSHE"
        """
        cls.get_active()._stock = stock

    @classmethod
    def get_current_stock(cls):
        return cls.get_active()._stock

    @classmethod
    def set_data_backend(cls, data_backend):
        """set current watching stock
        :param stock: "000002.XSHE"
        """
        cls.get_active()._data_backend = data_backend

    @classmethod
    def get_data_backend(cls):
        return cls.get_active()._data_backend


def set_data_backend(backend):
    ExecutionContext.set_data_backend(backend)


def set_current_stock(stock):
    ExecutionContext.set_current_stock(stock)


def set_current_date(date):
    ExecutionContext.set_current_date(date)


def symbol(order_book_id):
    """获取股票代码对应的名字
    :param order_book_id:
    :returns:
    :rtype:
    """
    data_backend = ExecutionContext.get_data_backend()
    return data_backend.symbol(order_book_id)
