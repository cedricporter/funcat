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

- 开盘价：`OPEN` `O` `o`
- 收盘价：`CLOSE` `C` `c`
- 最高价：`HIGH` `H` `h`
- 最低价：`LOW` `L` `l`
- 成交量：`VOLUME` `V` `v`

### 工具函数

- n天前的数据：`REF` `ref`
``` python
REF(C, 10)  # 10天前的收盘价
```

- 均线：`MA` `ma`
``` python
MA(C, 60)  # 60日均线
```

- 金叉判断：`CROSS` `cross`
``` python
CROSS(MA(C, 5), MA(C, 10))  # 5日均线上穿10日均线
```

- 两个序列取最小值：`MIN` `minimum`
``` python
MIN(O, C)  # K线实体的最低价
```

- 两个序列取最大值：`MAX` `maximum`
``` python
MAX(O, C)  # K线实体的最高价
```

- n天都满足条件：`EVERY` `every`
``` python
EVERY(C > MA(C, 5), 10)  # 最近10天收盘价都大于5日均线
```

- n天内满足条件的天数：`COUNT` `count`
``` python
COUNT(C > O, 10)  # 最近10天收阳线的天数
```

- n天内最大值：`HHV` `hhv`
``` python
HHV(MAX(O, C), 60)  # 最近60天K线实体的最高价
```

- n天内最小值：`LLV` `llv`
``` python
LLV(MIN(O, C), 60)  # 最近60天K线实体的最低价
```

- 求和n日数据 `SUM` `sum`
``` python
SUM(C, 10)  # 求和10天的收盘价
```

还有更多的技术指标还在实现中，欢迎提交pr一起实现。

## 自定义公式示例
[DMA指标](http://wiki.mbalib.com/wiki/DMA)。DMA指标（Different of Moving Average）又叫平行线差指标，是目前股市分析技术指标中的一种中短期指标，它常用于大盘指数和个股的研判。

``` python
M1 = 10
M2 = 50
M3 = 10

DDD = MA(CLOSE, M1) - MA(CLOSE, M2)
AMA = MA(DDD, M3)

print(DDD, AMA)
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

为了更高的性能，可以自定义Backend使用本地数据。这样可以极大地提高运行速度。

## TODO
- EMA
- MACD
- KDJ
- BOLL


## 通达信 

#### 行情函数

*   [X] HIGH(H):    最高价，返回该周期最高价。
*   [X] LOW(L):     最低价，返回该周期最低价。
*   [X] CLOSE(C):   收盘价，返回该周期收盘价。
*   [X] VOL(V):     成交量（手），返回该周期成交量。
*   [X] OPEN(O):    开盘价，返回该周期开盘价。
*   [ ] ADVANCE:    上涨家数，返回该周期上涨家数. (本函数仅对大盘有效)
*   [ ] DECLINE:    下跌家数，返回该周期下跌家数. (本函数仅对大盘有效)
*   [ ] AMOUNT:     成交额（元），返回该周期成交额.
*   [ ] VOLINSTK:   持仓量，返回期货该周期持仓量.
*   [ ] QHJSJ:      期货结算价 返回期货该周期结算价.
*   [ ] BUYVOL:     外盘（手），返回外盘，即时行情数据
*   [ ] SELVOL:     外盘（手），返回外盘
*   [ ] ISBUYORDER: 主动性买单，返回当前成交是否为主动性买单.用法: ISBUYORDER， 当本笔成交为主动性买盘时,返回1,否则为0
*   [ ] DHIGH:      不定周期最高价，返回该不定周期最高价.
*   [ ] DOPEN:      不定周期开盘价，返回该不定周期开盘价.
*   [ ] DLOW:       不定周期最低价，返回该不定周期最低价.
*   [ ] DCLOSE:     不定周期收盘价，返回该不定周期收盘价.
*   [ ] DVOL:       不定周期成交量价，返回该不定周期成交量价.
*   [ ] NAMELIKE:   模糊股票名称 返回股票名称是否以参数开头. 用法: if(NAMELIKE('ST'),x,y);
*   [ ] CODELIKE:   模糊股票代码 返回股票代码是否以参数开头. 用法: if(CODELIKE('600'),x,y);
*   [ ] INBLOCK:    属于某板块 返回股票是否属于某板块. 用法: if(INBLOCK('沪深300'),x,y);

#### 时间函数

*   [ ] PERIOD:     周期，取得周期类型. 结果从0到11,依次分别是1/5/15/30/60分钟,日/周/月,多分钟,多日,季,年.
*   [ ] DATE:       日期，取得该周期从1900以来的的年月日. 用法: DATE 例如函数返回1000101,表示2000年1月1日,DATE+19000000后才是真正的日期值
*   [ ] TIME:       时间，取得该周期的时分秒.用法:  TIME 函数返回有效值范围为(000000-235959)
*   [ ] YEAR:       年份，取得该周期的年份.
*   [ ] MONTH:      月份，取得该周期的月份.用法:  函数返回有效值范围为(1-12)
*   [ ] WEEKDAY:    星期，取得该周期的星期数.用法: WEEKDAY 函数返回有效值范围为(1-7)
*   [ ] DAY:        日，取得该周期的日期.用法: DAY 函数返回有效值范围为(1-31)
*   [ ] HOUR:       小时，取得该周期的小时数.用法: HOUR 函数返回有效值范围为(0-23),对于日线及更长的分析周期值为0
*   [ ] MINUTE:     分钟，取得该周期的分钟数.用法: MINUTE 函数返回有效值范围为(0-59),对于日线及更长的分析周期值为0
*   [ ] FROMOPEN:   分钟，求当前时刻距开盘有多长时间.用法: FROMOPEN FROMOPEN.返回当前时刻距开盘有多长时间,单位为分钟.例如:当前时刻为早上十点，则返回31.
*   [ ] TFILT:      分钟，对指定时间段的数据进行过滤,该时间段以外的数据无效. 用法: TFILT(X,D1,M1,D2,M2) 例如TFILT(CLOSE,1040101,1025,1040101,1345)表示在2004年1月1日的10:25到2004年1月1日的13:45的收盘价是有效的.周期以日为基本单位的,分时为0有效.
*   [ ] DATETODAY:  上指纪元，指定日期到1990.12.19的天数. 用法: DATETODAY(date) DATETODAY(date).返回date到1990.12.19的天数.有效日期为(901219-1341231) 例如:DATETODAY(901219)返回0.
*   [ ] DAYTODATE:  转换日期，求1990.12.19后第若干天的日期. 用法: DAYTODATE(N) DAYTODATE(N).返回1990.12.19后第N天的日期.有效天数为(0-20000) 例如:DAYTODATE(0)返回901219.
*   [ ] TIMETOSEC:  当日秒数，求指定时刻距0时有多长时间. 用法: TIMETOSEC(time) TIMETOSEC(time).返回time时刻距0时有多长时间,单位为秒.有效时间为(0-235959) 例如:TIMETOSEC(93000)返回34200.
*   [ ] SECTOTIME:  转换时间，求0时后若干秒是什么时间. 用法: SECTOTIME(N) SECTOTIME(N).返回0时后N秒是什么时间.有效秒数为(0-86399) 例如:SECTOTIME(34200)返回93000.

#### 引用函数

*   [ ] DRAWNULL:   无效数，返回无效数.用法： DRAWNULL 例如IF(CLOSE>REF(CLOSE,1),CLOSE,DRAWNULL)表示下跌时分析图上不画线
*   [ ] BACKSET:    向前赋值   将当前位置到若干周期前的数据设为1.用法: BACKSET(X,N),若X非0,则将当前位置到N周期前的数值设为1.例如:BACKSET(CLOSE>OPEN,2)若收阳则将该周期及前一周期数值设为1,否则为0
*   [ ] BARSCOUNT:  有效数据周期数   求总的周期数.用法: BARSCOUNT(X)第一个有效数据到当前的天数例如:BARSCOUNT(CLOSE)对于日线数据取得上市以来总交易日数,对于分笔成交取得当日成交笔数,对于1分钟线取得当日交易分钟数
*   [ ] CURRBARSCOUNT:  到最后交易日的周期数   求到最后交易日的周期数.用法: CURRBARSCOUNT 求到最后交易日的周期数
*   [ ] TOTALBARSCOUNT: 总的周期数   求总的周期数.用法: TOTALBARSCOUNT 求总的周期数
*   [ ] ISLASTBAR:  是否为最后一个周期   判断是否为最后一个周期.用法: ISLASTBAR 判断是否为最后一个周期
*   [ ] BARSLAST:   上一条件成立位置   上一次条件成立到当前的周期数.用法: BARSLAST(X):上一次X不为0到现在的天数例如:BARSLAST(CLOSE/REF(CLOSE,1)>=1.1)表示上一个涨停板到当前的周期数
*   [ ] BARSSINCE:  第一个条件成立位置   第一个条件成立到当前的周期数.用法: BARSSINCE(X):第一次X不为0到现在的天数例如:BARSSINCE(HIGH>10)表示股价超过10元时到当前的周期数
*   [ ] BARSSINCEN: N周期内首个条件成立位置 N周期内第一个条件成立到当前的周期数.
    用法: BARSSINCEN(X,N):N周期内第一次X不为0到现在的天数
    例如:BARSSINCEN(HIGH>10,10)表示10个周期内股价超过10元时到当前的周期数
*   [ ] BARSSINCE:  首个条件成立位置 第一个条件成立到当前的周期数.
    用法: BARSSINCE(X):第一次X不为0到现在的天数
    例如:BARSSINCE(HIGH>10)表示股价超过10元时到当前的周期数
*   [X] COUNT:      统计，统计满足条件的周期数.用法: COUNT(X,N),统计N周期中满足X条件的周期数,若N=0则从第一个有效值开始.例如:COUNT(CLOSE>OPEN,20)表示统计20周期内收阳的周期数
*   [ ] BARSLASTCOUNT:  统计条件连续成立次数，统计连续满足条件的周期数.用法: BARSLASTCOUNT(X),统计连续满足X条件的周期数.例如:BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
*   [ ] DMA:        动态移动平均，求动态移动平均.用法: DMA(X,A),求X的动态移动平均.算法: 若Y=DMA(X,A)则 Y=A*X+(1-A)*Y',其中Y'表示上一周期Y值,A必须小于1.例如:DMA(CLOSE,VOL/CAPITAL)表示求以换手率作平滑因子的平均价
*   [X] HHV:        最高值，求最高值。用法: HHV(X,N),求N周期内X最高值,N=0则从第一个有效值开始. 例如:HHV(HIGH,30)表示求30日最高价
*   [ ] HHVBARS:    上一高点位置，求上一高点到当前的周期数.用法: HHVBARS(X,N):求N周期内X最高值到当前周期数,N=0表示从第一个有效值开始统计 例如:HHVBARS(HIGH,0)求得历史新高到到当前的周期数
*   [ ] HOD:        高值名次，求高值名次.
    用法: HOD(X,N):求当前X数据是N周期内的第几个高值,N=0则从第一个有效值开始.
    例如:HOD(HIGH,20)返回是20日的第几个高价
*   [X] LLV:        最低值，求最低值.用法: LLV(X,N),求N周期内X最低值,N=0则从第一个有效值开始. 例如:LLV(LOW,0)表示求历史最低价
*   [ ] LLVBARS:    上一低点位置，求上一低点到当前的周期数.用法: LLVBARS(X,N):求N周期内X最低值到当前周期数,N=0表示从第一个有效值开始统计 例如:LLVBARS(HIGH,20)求得20日最低点到当前的周期数
*   [ ] LOD:        低值名次，求低值名次.
    用法: LOD(X,N):求当前X数据是N周期内的第几个低值,N=0则从第一个有效值开始.
    例如:LOD(LOW,20)返回是20日的第几个低价
*   [ ] REVERSE:    求相反数，求相反数.用法:REVERSE(X)返回-X.例如REVERSE(CLOSE)返回-CLOSE
*   [X] REF:        日前的，引用若干周期前的数据.用法: REF(X,A),引用A周期前的X值. 例如:REF(CLOSE,1)表示上一周期的收盘价,在日线上就是昨收
*   [ ] REFV:       日前的  引用若干周期前的数据(未作平滑处理).
    用法: REFV(X,A),引用A周期前的X值.A可以是变量.
    平滑处理：当引用不到数据时进行的操作。
    例如:REFV(CLOSE,BARSCOUNT(C)-1)表示第二根K线的收盘价.
*   [ ] REFX：       日后的 引用若干周期后的数据(未作平滑处理).
    用法: REFX(X,A),引用A周期后的X值.A可以是变量.
    平滑处理：当引用不到数据时进行的操作。
    例如:REFX(CLOSE,1)表示下一周期的收盘价,在日线上就是明天收盘价
*   [ ] REFXV：      日后的 引用若干周期后的数据(平滑处理).
    用法: REFXV(X,A),引用A周期后的X值.A可以是变量.
    平滑处理：当引用不到数据时进行的操作。此函数中，平滑时使用上一个周期的引用值。
    例如:TT:=IF(C>O,1,2);
    REFXV(CLOSE,TT);表示阳线引用下一周期的收盘价,阴线引用日后第二周期的收盘价.
*   [ ] REFDATE:    日   引用自1900年以来指定日期的数据.用法: REFDATE(X,A),引用A日期的X值. 例如:REFDATE(CLOSE,1011208)表示2001年12月08日的收盘价
*   [X] SUM:        累和   求总和.用法: SUM(X,N),统计N周期中X的总和,N=0则从第一个有效值开始.例如:SUM(VOL,0)表示统计从上市第一天以来的成交量总和
*   [ ] FILTER:     过滤   过滤连续出现的信号.用法:FILTER(X,N):X满足条件后，删除其后N周期内的数据置为0. 例如：FILTER(CLOSE>OPEN,5)查找阳线，5天内再次出现的阳线不被记录在内
*   [ ] FILTERX:    反向过滤 反向过滤连续出现的信号.
    用法:FILTERX(X,N):X满足条件后，将其前N周期内的数据置为0.
    例如：FILTERX(CLOSE>OPEN,5)查找阳线，前5天内出现过的阳线不被记录在内
*   [ ] TFILTER:    交易信号过滤 过滤连续出现的交易信号.
    用法:TFILTER(开仓,平仓,N);过滤掉开仓(平仓)信号发出后、下一个平仓(开仓)信号发出前的所有开仓(平仓)信号.
    N=1表示仅对开仓信号过滤;
    N=2表示仅对平仓信号过滤;
    N=0表示对开仓、平仓信号都过滤;
    例如：ENTERLONG:TFILTER(开仓,平仓,1);
    EXITLONG:TFILTER(开仓,平仓,2);
*   [ ] TTFILTER:   交易信号过滤 过滤多空交易信号.
    用法:TTFILTER(多头买入开仓,多头卖出平仓,空头卖出开仓,空头买入平仓,N);
    1.过滤掉多(空)开仓信号发出后、下一个多(空)平仓信号发出前的所有多(空)开仓信号.
    2.多(空)开仓信号发出且空(多)仓已建时,要发出一个平空(多)仓的信号.
    3.过滤掉多(空)平仓信号发出后、下一个多(空)开仓信号发出前的所有多(空)平仓信号.
    N=1表示仅对多头开仓信号过滤;
    N=2表示仅对多头平仓信号过滤;
    N=3表示仅对空头开仓信号过滤;
    N=4表示仅对空头平仓信号过滤;
    N=0表示对合并多空开仓、平仓信号;
    例如：ENTERLONG:TTFILTER(多头买入开仓,多头卖出平仓,空头卖出开仓,空头买入平仓,1);
    EXITLONG:TTFILTER(多头买入开仓,多头卖出平仓,空头卖出开仓,空头买入平仓,2);
    ENTERSHORT:TTFILTER(多头买入开仓,多头卖出平仓,空头卖出开仓,空头买入平仓,3);
    EXITSHORT:TTFILTER(多头买入开仓,多头卖出平仓,空头卖出开仓,空头买入平仓,4);
*   [ ] TR:         真实波幅 求真实波幅.
    用法: TR,求真实波幅.例如:ATR:=MA(TR,10);
    表示求真实波幅的10周期均值
*   [ ] SUMBARS:    累加到指定值的周期数   向前累加到指定值到现在的周期数.用法: SUMBARS(X,A):将X向前累加直到大于等于A,返回这个区间的周期数 例如:SUMBARS(VOL,CAPITAL)求完全换手到现在的周期数
*   [ ] SMA:        移动平均   返回移动平均用法:SMA(X,N,M):X的M日移动平均,M为权重,如Y=(X*M+Y'*(N-M))/N
*   [ ] TMA:        返回移动平均
    用法:TMA(X,N,M),如若Y=TMA(X,N,M) 则 Y=(N*Y'+M*X), 其中Y'表示上一周期Y值。初值为M*X
*   [X] MA:         简单移动平均   返回简单移动平均用法:MA(X,M):X的M日简单移动平均
*   [X] EMA:        指数移动平均   返回指数移动平均用法:EMA(X,M):X的M日指数移动平均
*   [ ] MEMA:       平滑移动平均   返回平滑移动平均用法:MEMA(X,M):X的M日平滑移动平均
*   [X] EXPMA:      指数移动平均   返回指数移动平均用法:EXPMA(X,M):X的M日指数移动平均
*   [ ] EXPMEMA:    指数平滑移动平均   返回指数平滑移动平均用法:EXPMEMA(X,M):X的M日指数平滑移动平均
*   [ ] XMA:        偏移移动平均   返回偏移移动平均用法:XMA(X,M):X的M日偏移移动平均
*   [ ] RANGE:      介于某一范围之间   RANGE(A,B,C):A在B和C范围之间.用法: RANGE(A,B,C)表示A大于B同时小于C时返回1，否则返回0
*   [ ] CONST:      取值设为常数   CONST(A):取A最后的值为常量.用法: CONST(INDEXC)表示取大盘现价
*   [ ] TOPRANGE:   当前值是近多少周期内的最大值.
    用法: TOPRANGE(X):X是近多少周期内X的最大值
    例如:TOPRANGE(HIGH)表示当前最高价是近多少周期内的最高价
*   [ ] LOWRANGE:   当前值是近多少周期内的最小值.
    用法: LOWRANGE(X):X是近多少周期内X的最小值
    例如:LOWRANGE(LOW)表示当前最高价是近多少周期内的最小价
*   [ ] FINDHIGH:   寻找指定周期内的特定最大值 N周期前的M周期内的第T个最大值.
    用法: FINDHIGH(VAR,N,M,T):VAR在N日前的M天内第T个最高价
*   [ ] FINDHIGHBARS:   寻找指定周期内的特定最大值 N周期前的M周期内的第T个最大值到当前周期的周期数.
    用法: FINDHIGHBARS (VAR,N,M,T):VAR在N日前的M天内第T个最高价到当前周期的周期数
*   [ ] FINDLOW:    寻找指定周期内的特定最小值 N周期前的M周期内的第T个最小值.
    用法: FINDLOW(VAR,N,M,T):VAR在N日前的M天内第T个最低价
*   [ ] FINDLOWBARS:    寻找指定周期内的特定最小值 N周期前的M周期内的第T个最小值到当前周期的周期数.
    用法: FINDLOWBARS(VAR,N,M,T):VAR在N日前的M天内第T个最低价到当前周期的周期数.
   
### 逻辑函数

*   [X] CROSS:      上穿，两条线交叉.用法: CROSS(A,B)表示当A从下方向上穿过B时返回1,否则返回0 例如:CROSS(MA(CLOSE,5),MA(CLOSE,10))表示5日均线与10日均线交金叉
*   [ ] LONGCROSS:  持续周期后上穿，两条线维持一定周期后交叉. 用法:LONGCROSS(A,B,N)表示A在N周期内都小于B，本周期从下方向上穿过B时返回1，否则返回0
*   [ ] UPNDAY:     连涨，返回是否连涨周期数.用法: UPNDAY(CLOSE,M) 表示连涨M个周期
*   [ ] DOWNNDAY:   连跌，返回是否连跌周期.用法: DOWNNDAY(CLOSE,M) 表示连跌M个周期
*   [ ] NDAY:       连大，返回是否持续存在X>Y用法: NDAY(CLOSE,OPEN,3) 表示连续3日收阳线
*   [ ] EXIST:      存在，是否存在.用法: EXIST(CLOSE>OPEN,10)  表示前10日内存在着阳线
*   [X] EVERY:      一直存在，一直存在.用法: EVERY(CLOSE>OPEN,10)  表示前10日内一直阳线
*   [ ] LAST:       持续存在，LAST(X,A,B):持续存在.用法: LAST(CLOSE>OPEN,10,5)  表示从前10日到前5日内一直阳线 若A为0,表示从第一天开始,B为0,表示到最后日止
*   [ ] TESTSKIP:   是否就此返回，TESTSKIP(A):不满足A则直接返回.用法: TESTSKIP(A)  表示如果不满足条件A则改公式直接返回，不再计算接下来的表达式

### 算术函数

*   [ ] NOT:        取反，求逻辑非.用法: NOT(X)返回非X,即当X=0时返回1,否则返回0; 例如:NOT(ISUP)表示平盘或收阴
*   [ ] IF :        辑判断，根据条件求不同的值.用法: IF(X,A,B)若X不为0则返回A,否则返回B; 例如:IF(CLOSE>OPEN,HIGH,LOW)表示该周期收阳则返回最高值,否则返回最低值
*   [ ] IFF:        逻辑判断，根据条件求不同的值.用法: IFF(X,A,B)若X不为0则返回A,否则返回B 例如:IFF(CLOSE>OPEN,HIGH,LOW)表示该周期收阳则返回最高值,否则返回最低值
*   [ ] IFN:        逻辑判断，根据条件求不同的值.用法: IFN(X,A,B)若X不为0则返回B,否则返回A 例如:IFN(CLOSE>OPEN,HIGH,LOW)表示该周期收阴则返回最高值,否则返回最低值
*   [X] MAX:        较大值，求最大值.用法: MAX(A,B)返回A和B中的较大值 例如:MAX(CLOSE-OPEN,0)表示若收盘价大于开盘价返回它们的差值,否则返回0
*   [X] MIN:        较小值，求最小值.用法: MIN(A,B)返回A和B中的较小值 例如:MIN(CLOSE,OPEN)返回开盘价和收盘价中的较小值

### 数学函数

*   [ ] ACOS:       反余弦   反余弦值.用法: ACOS(X)返回X的反余弦值
*   [ ] ASIN:       反正弦   反正弦值.用法: ASIN(X)返回X的反正弦值
*   [ ] ATAN:       反正切   反正切值.用法: ATAN(X)返回X的反正切值
*   [ ] COS:        余弦   余弦值.用法: COS(X)返回X的余弦值
*   [ ] SIN:        正弦   正弦值.用法: SIN(X)返回X的正弦值
*   [ ] TAN:        正切   正切值.用法: TAN(X)返回X的正切值
*   [ ] EXP:        指数   指数.用法: EXP(X)为e的X次幂 例如:EXP(CLOSE)返回e的CLOSE次幂
*   [ ] LN:         自然对数   求自然对数.用法: LN(X)以e为底的对数 例如:LN(CLOSE)求收盘价的对数
*   [ ] LOG:        对数   求10为底的对数.用法: LOG(X)取得X的对数; 例如:LOG(100)等于2
*   [ ] SQRT:       开方   开平方.用法: SQRT(X)为X的平方根; 例如:SQRT(CLOSE)收盘价的平方根
*   [ ] ABS:        绝对值   求绝对值.用法: ABS(X)返回X的绝对值; 例如:ABS(-34)返回34
*   [ ] POW:        乘幂   乘幂.用法: POW(A,B)返回A的B次幂; 例如:POW(CLOSE,3)求得收盘价的3次方
*   [ ] CEILING:    向上舍入   向上舍入.用法:CEILING(A)返回沿A数值增大方向最接近的整数例如:CEILING(12.3)求得13,CEILING(-3.5)求得-3
*   [ ] FLOOR:      向下舍入   向下舍入.用法:FLOOR(A)返回沿A数值减小方向最接近的整数例如:FLOOR(12.3)求得12,FLOOR(-3.5)求得-4
*   [ ] INTPART:    取整   取整.用法:INTPART(A)返回沿A绝对值减小方向最接近的整数例如:INTPART(12.3)求得12,INTPART(-3.5)求得-3
*   [ ] BETWEEN:    介于   介于.用法:BETWEEN(A,B,C)表示A处于B和C之间时返回1，否则返回0例如:BETWEEN(CLOSE,MA(CLOSE,10),MA(CLOSE,5))表示收盘价介于5日均线和10日均线之间
*   [ ] FRACPART:   小数部分.用法:FRACPART(X),返回X的小数部分
*   [ ] ROUND:      四舍五入.用法:ROUND(X),返回X四舍五入到个位的数值
*   [ ] SIGN:       取符号.用法:SIGN(X),返回X的符号.当X>0,X=0,X<0分别返回1,0,-1
*   [ ] MOD:        取模.用法:MOD(M,N),返回M关于N的模(M除以N的余数);例如:MOD(5,3)返回2
*   [ ] RAND:       取随机数.用法:RAND(N),返回一个范围在1-N的随机整数

### 统计函数

*   [ ] AVEDEV:     平均绝对方差    AVEDEV(X,N) 返回平均绝对方差
*   [ ] DEVSQ:      数据偏差平方和   DEVSQ(X,N) 返回数据偏差平方和
*   [ ] FORCAST:    线性回归预测值   FORCAST(X,N) 返回线性回归预测值
*   [ ] SLOPE:      线性回归斜率   SLOPE(X,N) 返回线性回归斜率
*   [ ] STD:        估算标准差   STD(X,N) 返回估算标准差
*   [ ] STDP:       总体标准差   STDP(X,N) 返回总体标准差
*   [ ] VAR:        估算样本方差   VAR(X,N) 返回估算样本方差
*   [ ] VARP:       总体样本方差   VARP(X,N) 返回总体样本方差
*   [ ] COVAR:      协方差,COVAR(X,Y,N) 返回X和Y的N周期的协方差
*   [ ] RELATE:     相关系数，RELATE(X,Y,N) 返回X和Y的N周期的相关系数
*   [ ] BETA:       β(Beta)系数，BETA(N) 返回当前证券N周期收益与大盘收益相比的贝塔系数
*   [ ] BETAEX:     相关放大系数，BETAEX(X,Y,N) 返回X与Y的N周期的相关放大系数

### 横向统计

*   [ ] BLOCKSETNUM:    板块股票个数，用法:BLOCKSETNUM(板块名称),返回该板块股票个数
*   [ ] HORCALC:    多股统计，用法:HORCALC(板块名称,数据项,计算方式,权重),
    数据项:100-HIGH,101-OPEN,102-LOW,103-CLOSE,104-VOL,105-涨幅
    计算方式:0-累加,1-排名次
    权重:0-总股本,1-流通股本,2-等同权重,3-流通市值
*   [ ] INSORT:     板块排序选股，用法:INSORT(板块名称,指标名称,指标线,升降序),返回该股在板块中的排序序号，例如:INSORT('房地产','KDJ',3,0)表示该股的KDJ指标第三个输出即J之值在房地产板块中的排名,最后一个参数为0表示降序排名
*   [ ] INSUM:      板块指标统计，用法:INSUM(板块名称,指标名称,指标线,计算类型),返回板块各成分该指标相应输出安计算类型得到的计算值.计算类型:0-累加,1-平均数,2-最大值,3-最小值.
    例如:INSUM('房地产','KDJ',3,0)表示房地产板块中所有股票的KDJ指标第三个输出即J之值的累加值

### 形态函数

*   [ ] COST:       成本分布   成本分布情况.用法:COST(10),表示10%获利盘的价格是多少,即有10%的持仓量在该价格以下,其余90%在该价格以上,为套牢盘，该函数仅对日线分析周期有效
*   [ ] PEAK:       波峰值   前M个ZIG转向波峰值.
    用法:PEAK(K,N,M)表示之字转向ZIG(K,N)的前M个波峰的数值,M必须大于等于1例如:PEAK(1,5,1)表示%5最高价ZIG转向的上一个波峰的数值
*   [ ] PEAKBARS:   波峰位置   前M个ZIG转向波峰到当前距离.用法:PEAKBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波峰到当前的周期数,M必须大于等于1例如:PEAK(0,5,1)表示%5开盘价ZIG转向的上一个波峰到当前的周期数
*   [ ] SAR:        抛物转向   抛物转向.用法:SAR(N,S,M),N为计算周期,S为步长,M为极值例如SAR(10,2,20)表示计算10日抛物转向,步长为2%,极限值为20%
*   [ ] SARTURN:    抛物转向点   抛物转向点.用法:SARTURN(N,S,M),N为计算周期,S为步长,M为极值,若发生向上转向则返回1,若发生向下转向则返回-1,否则为0，其用法与SAR函数相同
*   [ ] TROUGH:     波谷值   前M个ZIG转向波谷值.
    用法:TROUGH(K,N,M)表示之字转向ZIG(K,N)的前M个波谷的数值,M必须大于等于1例如:TROUGH(2,5,2)表示%5最低价ZIG转向的前2个波谷的数值
*   [ ] TROUGHBARS: 波谷位置   前M个ZIG转向波谷到当前距离.
    用法:TROUGHBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波谷到当前的周期数,M必须大于等于1例如:TROUGH(2,5,2)表示%5最低价ZIG转向的前2个波谷到当前的周期数
*   [ ] WINNER:     获利盘比例   获利盘比例.用法:WINNER(CLOSE),表示以当前收市价卖出的获利盘比例,例如返回0.1表示10%获利盘;WINNER(10.5)表示10.5元价格的获利盘比例，该函数仅对日线分析周期有效
*   [ ] LWINNER:    近期获利盘比例   近期获利盘比例.  用法:LWINNER(5,CLOSE),表示最近5天的那部分成本以当前收市价卖出的获利盘比例例如返回0.1表示10%获利盘
*   [ ] PWINNER:    远期获利盘比例   远期获利盘比例.   用法:PWINNER(5,CLOSE),表示5天前的那部分成本以当前收市价卖出的获利盘比例例如返回0.1表示10%获利盘
*   [ ] CostEX:     区间成本   区间成本.用法:CostEX(CLOSE, REF(CLOSE)),表示近两日收盘价格间筹码的成本,例如返回10表示区间成本为20元该函数仅对日线分析周期有效
*   [ ] PPART:      远期成本分布比例   远期成本分布比例.
    用法:PPART(10),表示10前的成本占总成本的比例，0.2表示20%
*   [ ] ZIG:        之字转向   之字转向.用法:ZIG(K,N),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,其余:数组信息例如:ZIG(3,5)表示收盘价的5%的ZIG转向
*   [ ] NewSAR:     新抛物转向函数
    用法:NewSAR(N,S),N为起始统计天数,S为加速因子
    例如NewSAR(10,2)表示从10日后开始统计,加速因子为2的抛物转向
*   [ ] LFS:        返回个股锁定因子
