from datetime import datetime
from vnpy.trader.constant import Interval, Exchange
from vnpy_ctastrategy.backtesting import MultiSymbolBacktestingEngine

# 1. 初始化引擎
engine = MultiSymbolBacktestingEngine()

from  vnpy_ctastrategy.strategies import TailTradeStrategy

from vnpy.trader.datafeed import get_datafeed

datafeed = get_datafeed()

# 2. 设置参数 (参考原代码 set_parameters)
engine.set_parameters(
    vt_symbol="600000.SH", # 基准合约
    interval=Interval.DAILY,
    start=datetime(2025, 1, 1),
    end=datetime(2026, 1, 29),
    rate=0.0003 + 0.001,   # 佣金 + 印花税 (A股特有)
    slippage=0.01,         # 滑点
    size=100,
    pricetick=0.01,
    capital=1000000
)

# 3. 准备股票池
stock_list = datafeed.get_all_stocks()["ts_code"]

# 4. 加载数据并运行
engine.load_market_data(stock_list)
engine.add_strategy(TailTradeStrategy, {})
engine.run_market_backtesting()

# 5. 计算结果 (利用原代码计算逻辑)
engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()