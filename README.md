# Funcat
提供 Python 公式选股。

使用同花顺、通达信等公式，做技术分析，表达十分简洁。

苦于 Python 缺乏这种领域特定语言，所以用 Python 实现了一套。

## 安装
```
pip install funcat
```

## quick start
``` python
from funcat import *
from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

# 设置目前天数为2017年1月4日
T("20170104")
# 设置关注股票为上证指数
S("000001.XSHG")

# 打印 Open High Low Close
>>> print(O, H, L, C)
3133.79 3160.1 3130.11 3158.79
# 当天涨幅
>>> C / C[1] - 1
0.0072929156356
# 打印60日均线
>>> MA(C, 60)
3154.78333333
# 判断收盘价是否大于60日均线
>>> C > MA(C, 60)
True
# 30日最高价
>>> HHV(H, 30)
3301.21
# 最近30日，收盘价 Close 大于60日均线的天数
>>> COUNT(C > MA(C, 60), 30)
17
# 10日均线上穿
>>> CROSS(MA(C, 10), MA(C, 20))
False
```

## 选股
``` python
# 选出涨停股
loop(
    lambda : C / C[1] - 1 >= 0.995,
    limit_start=20161231,
)
''' output
lambda : C / C[1] - 1 >= 0.0995,
[20170104]
20170104 000045.XSHE 000045.XSHE[深纺织Ａ]
20170104 000585.XSHE 000585.XSHE[东北电气]
20170104 000595.XSHE 000595.XSHE[宝塔实业]
20170104 000695.XSHE 000695.XSHE[滨海能源]
20170104 000710.XSHE 000710.XSHE[天兴仪表]
20170104 000755.XSHE 000755.XSHE[山西三维]
...
'''

# 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
def callback(date, order_book_id, symbol):
    print("Cool, 在", date, "选出", order_book_id, symbol)

loop(
    lambda : (EVERY(V < MA(V, 20) / 2, 3) and EVERY(L < MA(C, 20), 3) and EVERY(H > MA(C, 20), 3)),
    limit_start=20161231,
    callback=callback,
)
'''
output
[20170104]
Cool, 在 20170104 选出 002633.XSHE 002633.XSHE[申科股份]
Cool, 在 20170104 选出 600857.XSHG 600857.XSHG[宁波中百]
'''
```
