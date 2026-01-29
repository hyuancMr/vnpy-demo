# 忽略各模块的警告信息
import warnings
warnings.filterwarnings("ignore")

# 加载所需使用的模块
from datetime import datetime

from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.database import get_database, DB_TZ
from vnpy.trader.constant import Interval
from vnpy.trader.object import BarData, HistoryRequest
from vnpy.trader.utility import extract_vt_symbol
from vnpy.trader.setting import SETTINGS

# 创建对象实例
datafeed = get_datafeed()

database = get_database()

# 要下载数据的合约代码
vt_symbols = datafeed.get_all_stocks()

# 遍历列表执行下载
for vt_symbol in vt_symbols["ts_code"]:
    # 拆分合约代码和交易所
    symbol, exchange = extract_vt_symbol(vt_symbol)

    # 创建历史数据请求对象
    req: HistoryRequest = HistoryRequest(
        symbol=symbol,
        exchange=exchange,
        start=datetime(2025, 1, 1),
        end=datetime(2026, 1, 29),
        interval=Interval.DAILY        # 这里下载最常用的1分钟K线
    )

    # 从数据服务下载数据
    bars: list[BarData] = datafeed.query_bar_history(req)

    # 如果下载成功则保存
    if bars:
        database.save_bar_data(bars)
        print(f"下载数据成功：{vt_symbol}，总数据量：{len(bars)}")
    # 否则失败则打印信息
    else:
        print(f"下载数据失败：{vt_symbol}")