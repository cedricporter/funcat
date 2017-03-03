# Funcat
Funcat 将同花顺、通达信等的公式移植到了 Python 中。

同花顺、通达信等公式的表达十分简洁，适合做技术分析。

苦于 Python 缺乏这种领域特定语言的表达能力，所以用 Python 基于 numpy 实现了一套。

## 安装
```
pip install -U funcat
```

## notebooks 教程
- [quick-start](https://github.com/cedricporter/funcat/blob/master/notebooks/funcat-tutorial.ipynb)

## API
### 行情变量

- 开盘价：`OPEN` `O`
- 收盘价：`CLOSE` `C`
- 最高价：`HIGH` `H`
- 最低价：`LOW` `L`
- 成交量：`VOLUME` `V`

### 工具函数

- n天前的数据：`REF`
``` python
REF(C, 10)  # 10天前的收盘价
```

- 均线：`MA`
``` python
MA(C, 60)  # 60日均线
```

- 金叉判断：`CROSS`
``` python
CROSS(MA(C, 5), MA(C, 10))  # 5日均线上穿10日均线
```

- 两个序列取最小值：`MIN`
``` python
MIN(O, C)  # K线实体的最低价
```

- 两个序列取最大值：`MAX`
``` python
MAX(O, C)  # K线实体的最高价
```

- n天都满足条件：`EVERY`
``` python
EVERY(C > MA(C, 5), 10)  # 最近10天收盘价都大于5日均线
```

- n天内满足条件的天数：`COUNT`
``` python
COUNT(C > O, 10)  # 最近10天收阳线的天数
```

- n天内最大值：`HHV`
``` python
HHV(MAX(O, C), 60)  # 最近60天K线实体的最高价
```

- n天内最小值：`LLV`
``` python
LLV(MIN(O, C), 60)  # 最近60天K线实体的最低价
```

- 求和n日数据 `SUM`
``` python
SUM(C, 10)  # 求和10天的收盘价
```

- 求绝对值 `ABS`
``` python
ABS(C - O)
```

还有更多的技术指标还在实现中，欢迎提交pr一起实现。

## 自定义公式示例
[KDJ指标](http://wiki.mbalib.com/wiki/%E9%9A%8F%E6%9C%BA%E6%8C%87%E6%A0%87)。随机指标（KDJ）由 George C．Lane 创制。它综合了动量观念、强弱指标及移动平均线的优点，用来度量股价脱离价格正常范围的变异程度。

``` python
N, M1, M2 = 9, 3, 3

RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
K = EMA(RSV, (M1 * 2 - 1))
D = EMA(K, (M2 * 2 - 1))
J = K * 3 - D * 2

print(K, D, J)
```


## 选股

``` python
from funcat import *


# 选出涨停股
select(
    lambda : C / C[1] - 1 >= 0.0995,
    start_date=20161231,
	end_date=20170104,
)

'''
[20170104]
20170104 000017.XSHE 000017.XSHE[深中华A]
20170104 000026.XSHE 000026.XSHE[飞亚达Ａ]
20170104 000045.XSHE 000045.XSHE[深纺织Ａ]
20170104 000585.XSHE 000585.XSHE[东北电气]
20170104 000595.XSHE 000595.XSHE[宝塔实业]
20170104 000678.XSHE 000678.XSHE[襄阳轴承]
...
'''


# 选出最近30天K线实体最高价最低价差7%以内，最近100天K线实体最高价最低价差大于25%，
# 最近10天，收盘价大于60日均线的天数大于3天
select(
    lambda : (HHV(MAX(C, O), 30) / LLV(MIN(C, O), 30) - 1 < 0.07
              and HHV(MAX(C, O), 100) / LLV(MIN(C, O), 100) - 1 > 0.25
              and COUNT(C > MA(C, 60), 10) > 3
             ),
    start_date=20161220,
)

'''
[20170104]
20170104 600512.XSHG 600512.XSHG[腾达建设]
[20170103]
[20161230]
20161230 000513.XSHE 000513.XSHE[丽珠集团]
...
'''


# 选出最近3天每天的成交量小于20日成交量均线，最近3天最低价低于20日均线，最高价高于20日均线
# 自定义选股回调函数
def callback(date, order_book_id, symbol):
    print("Cool, 在", date, "选出", order_book_id, symbol)


select(
    lambda : (EVERY(V < MA(V, 20) / 2, 3) and EVERY(L < MA(C, 20), 3) and EVERY(H > MA(C, 20), 3)),
    start_date=20161231,
    callback=callback,
)

'''
[20170104]
Cool, 在 20170104 选出 002633.XSHE 002633.XSHE[申科股份]
Cool, 在 20170104 选出 600857.XSHG 600857.XSHG[宁波中百]
...
'''
```

## 单股票研究
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

## DataBackend
默认实现了一个从 tushare 上面实时拉数据选股的 Backend。

还有一个 [RQAlpha](https://github.com/ricequant/rqalpha) 的 Backend，就可以在 RQAlpha 回测引擎中使用 funcat 的 API。

为了更高的性能，可以自定义Backend使用本地数据。这样可以极大地提高运行速度。

## TODO
talib常用指标
- MACD
- BOLL
- SAR
- IF
