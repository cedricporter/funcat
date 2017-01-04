#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from __future__ import print_function

import numpy as np

from .context import ExecutionContext, set_current_stock, set_current_date, symbol
from .utils import getsourcelines, FormulaException, get_int_date


def suppress_numpy_warn(func):
    def wrapper(*args, **kwargs):
        try:
            old_settings = np.seterr(all='ignore')
            return func(*args, **kwargs)
        finally:
            np.seterr(**old_settings)  # reset to default
    return wrapper


def choose(order_book_id, func, callback):
    set_current_stock(order_book_id)
    try:
        if func():
            date = ExecutionContext.get_current_date()
            callback(date, order_book_id, symbol(order_book_id))
    except FormulaException as e:
        pass


@suppress_numpy_warn
def loop(func, limit_start="2016-10-01", limit_end=None, max_date="2050-01-01", callback=print):
    print(getsourcelines(func))
    data_backend = ExecutionContext.get_data_backend()
    order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=data_backend.get_start_date(), end=max_date)
    for idx, date in enumerate(reversed(trading_dates)):
        if limit_end and date > get_int_date(limit_end):
            continue
        if date < get_int_date(limit_start):
            break
        set_current_date(str(date))
        print("[{}]".format(date))

        for order_book_id in order_book_id_list:
            choose(order_book_id, func, callback)

    print("")
