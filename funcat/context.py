# -*- coding: utf-8 -*-
#

import datetime

import six

from .utils import get_int_date


class ExecutionContext(object):
    stack = []

    def __init__(self, date=None, order_book_id=None, data_backend=None, freq="1d", start_date=datetime.date(1900, 1, 1)):
        self._current_date = self._convert_date_to_int(date)
        self._start_date = self._convert_date_to_int(start_date)
        self._order_book_id = order_book_id
        self._data_backend = data_backend
        self._freq = freq

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
        self._pop()

    def _convert_date_to_int(self, date):
        if isinstance(date, six.string_types):
            date = get_int_date(date)
        elif isinstance(date, datetime.date):
            date = int(date.strftime("%Y%m%d"))
        return date

    def _set_current_date(self, date):
        self._current_date = self._convert_date_to_int(date)

    def _set_start_date(self, date):
        self._start_date = self._convert_date_to_int(date)

    @classmethod
    def get_active(cls):
        return cls.stack[-1]

    @classmethod
    def set_current_date(cls, date):
        """set current simulation date
        :param date: string date, "2016-01-04"
        """
        cls.get_active()._set_current_date(date)

    @classmethod
    def get_current_date(cls):
        return cls.get_active()._current_date

    @classmethod
    def set_start_date(cls, date):
        cls.get_active()._set_start_date(date)

    @classmethod
    def get_start_date(cls):
        return cls.get_active()._start_date

    @classmethod
    def set_current_security(cls, order_book_id):
        """set current watching order_book_id
        :param order_book_id: "000002.XSHE"
        """
        cls.get_active()._order_book_id = order_book_id

    @classmethod
    def get_current_freq(cls):
        return cls.get_active()._freq

    @classmethod
    def set_current_freq(cls, freq):
        cls.get_active()._freq = freq

    @classmethod
    def get_current_security(cls):
        return cls.get_active()._order_book_id

    @classmethod
    def set_data_backend(cls, data_backend):
        """set current watching order_book_id
        :param order_book_id: "000002.XSHE"
        """
        cls.get_active()._data_backend = data_backend

    @classmethod
    def get_data_backend(cls):
        return cls.get_active()._data_backend


def set_data_backend(backend):
    ExecutionContext.set_data_backend(backend)


def set_current_security(order_book_id):
    ExecutionContext.set_current_security(order_book_id)


def set_start_date(date):
    ExecutionContext.set_start_date(date)


def set_current_date(date):
    ExecutionContext.set_current_date(date)


def set_current_freq(freq):
    ExecutionContext.set_current_freq(freq)


def symbol(order_book_id):
    """获取股票代码对应的名字
    :param order_book_id:
    :returns:
    :rtype:
    """
    data_backend = ExecutionContext.get_data_backend()
    return data_backend.symbol(order_book_id)
