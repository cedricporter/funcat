#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

from funcat import *


def test_000001():
    from funcat.data.tushare_backend import TushareDataBackend
    set_data_backend(TushareDataBackend("2016-01-01"))

    T("20161216")
    S("000001.XSHG")
    assert np.equal(round(c.value, 2), 3122.98)
    assert np.equal(round(o[2].value, 2), 3149.38)
    assert np.equal(round((c - o).value, 2), 11.47)
    assert np.equal(round((c - o)[2].value, 2), -8.85)
    assert np.equal(round(((c / c[1] - 1) * 100).value, 2), 0.17)
    assert np.equal(round(MA(C, 60)[2].value, 2), 3131.08)
    assert COUNT(C > O, 5) == 2

if __name__ == "__main__":
    print(123)
    # test_000001()
    print(MA(MA(C, 10), 20))
    print(REF(MA(MA(C, 60), 60), 10))
