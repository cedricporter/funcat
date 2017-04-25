# -*- coding: utf-8 -*-
#
from funcat.data.backend import DataBackend
from funcat.utils import get_str_date_from_int, get_int_date, FormulaException

from functools import lru_cache


class RQDataBackend(DataBackend):
    def __init__(self):
        import rqdatac
        self.rqdatac = rqdatac

    @staticmethod
    def convert_date_to_int(dt):
        t = dt.year * 10000 + dt.month * 100 + dt.day
        t *= 1000000
        return t

    @staticmethod
    def convert_dt_to_int(dt):
        t = RQDataBackend.convert_date_to_int(dt)
        t += dt.hour * 10000 + dt.minute * 100 + dt.second
        return t

    @lru_cache(4096)
    def get_price(self, order_book_id, start, end, freq):
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)

        df = self.rqdatac.get_price(order_book_id, start_date=start, end_date=end, frequency=freq)
        suspended_df = self.rqdatac.is_suspended(order_book_id, start_date=start, end_date=end)

        if suspended_df is None:
            raise FormulaException("missing data {}".format(order_book_id))

        df["suspended"] = suspended_df[order_book_id]
        df = df[df["suspended"] == False]

        df = df.reset_index()
        df["datetime"] = df["index"].apply(RQDataBackend.convert_dt_to_int)
        del df["index"]

        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        order_book_id_list = sorted(self.rqdatac.all_instruments("CS").order_book_id.tolist())
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        start = max(start, 20050101)
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        dates = self.rqdatac.get_trading_dates(start, end)
        trading_dates = [get_int_date(date) for date in dates]
        return trading_dates

    @lru_cache(4096)
    def symbol(self, order_book_id):
        return "{}[{}]".format(order_book_id, self.rqdatac.instruments(order_book_id).symbol)
