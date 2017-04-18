# -*- coding: utf-8 -*-
#

from __future__ import print_function

import datetime
import numpy as np

from .context import ExecutionContext, set_current_security, set_current_date, symbol
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
    set_current_security(order_book_id)
    try:
        if func():
            date = ExecutionContext.get_current_date()
            callback(date, order_book_id, symbol(order_book_id))
    except FormulaException as e:
        pass


@suppress_numpy_warn
def select(func, start_date="2016-10-01", end_date=None, callback=print):
    print(getsourcelines(func))
    start_date = get_int_date(start_date)
    if end_date is None:
        end_date = datetime.date.today()
    data_backend = ExecutionContext.get_data_backend()
    order_book_id_list = data_backend.get_order_book_id_list()
    trading_dates = data_backend.get_trading_dates(start=start_date, end=end_date)
    for idx, date in enumerate(reversed(trading_dates)):
        if end_date and date > get_int_date(end_date):
            continue
        if date < get_int_date(start_date):
            break
        set_current_date(str(date))
        print("[{}]".format(date))

        for order_book_id in order_book_id_list:
            choose(order_book_id, func, callback)

    print("")
