#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from __future__ import division

import inspect
import datetime

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


class FormulaException(Exception):
    pass


def wrap_formula_exc(func):
    def wrapper(*args, **kwargs):
        try:
            # print(func, args, kwargs)
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            raise FormulaException(e)

    return wrapper


def getsourcelines(func):
    try:
        source_code = "".join(inspect.getsourcelines(func)[0]).strip()
        return source_code
    except:
        return ""


def get_int_date(date):
    if isinstance(date, int):
        return date

    try:
        return int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d"))
    except:
        pass

    try:
        return int(datetime.datetime.strptime(date, "%Y%m%d").strftime("%Y%m%d"))
    except:
        pass


def get_str_date_from_int(date_int):
    try:
        date_int = int(date_int)
    except ValueError:
        date_int = int(date_int.replace("-", ""))
    year = date_int // 10000
    month = (date_int % 10000) // 100
    day = date_int % 100

    return "%d-%02d-%02d" % (year, month, day)


def get_date_from_int(date_int):
    date_str = get_str_date_from_int(date_int)

    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
