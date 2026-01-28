from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
from datetime import time

class TailTradeStrategy(CtaTemplate):
    """
    A股尾盘选股策略
    逻辑：14:50 判断当前价格是否高于均线且放量，若是则买入。
    次日 09:35 自动平仓。
    """
    author = "Coding Assistant"

    # 参数定义
    fast_window = 10
    slow_window = 20
    fixed_size = 100

    # 变量定义
    fast_ma = 0.0
    slow_ma = 0.0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        """策略初始化"""
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """策略启动"""
        self.write_log("策略启动")

    def on_stop(self):
        """策略停止"""
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """Tick更新，用于BarGenerator合成"""
        self.bg.update_tick(tick)

    # 在策略类中添加代码过滤逻辑
    def on_bar(self, bar: BarData):
        # 过滤逻辑：剔除 300 和 688 开头的股票
        symbol_code = bar.symbol
        if symbol_code.startswith("300") or symbol_code.startswith("688"):
            return

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        # 技术逻辑：价格 > 5日均线 且 14:50 成交量 > 过去5周期平均成交量的1.5倍
        avg_volume = am.volume[:-1].mean() # 获取历史平均成交量
        current_time = bar.datetime.time()

        if time(14, 50) <= current_time <= time(14, 57):
            if self.pos == 0:
                # 这里的 1.5 倍是放量系数
                if bar.close_price > am.sma(5) and bar.volume > avg_volume * 1.5:
                    self.buy(bar.close_price + 0.02, self.fixed_size)

    def on_order(self, order: OrderData):
        pass

    def on_trade(self, trade: TradeData):
        self.put_event()