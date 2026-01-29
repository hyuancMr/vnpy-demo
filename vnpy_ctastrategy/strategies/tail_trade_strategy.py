from vnpy_ctastrategy import CtaTemplate
from vnpy.trader.constant import Direction, Offset, Interval
from vnpy.trader.object import BarData, TickData, OrderData, TradeData

class TailTradeStrategy(CtaTemplate):
    """全市场尾盘筛选策略"""
    
    # 策略参数
    capital_per_stock = 20000  # 每只股票分配资金
    stock_count = 5            # 筛选数量
    
    def __init__(self, cta_engine, strategy_name, vt_symbols, setting):
        super().__init__(cta_engine, strategy_name, vt_symbols, setting)
        self.active_stocks = []  # 当前持仓列表
        
    def on_init(self):
        self.write_log("策略初始化")

    def on_start(self):
        self.write_log("策略启动")

    def on_market_bars(self, bars: dict[str, BarData]):
        """
        核心调用逻辑：由引擎每分钟调用一次，传入当前分钟全市场的Bar
        """
        dt = list(bars.values())[0].datetime
        
        # 1. 早上 09:31 集合竞价后立即卖出昨日持仓
        if dt.hour == 9 and dt.minute == 31:
            self.sell_all_holdings(bars)
            
        # 2. 下午 14:55 执行筛选逻辑
        if dt.hour == 14 and dt.minute == 55:
            self.screen_and_buy(bars)

    def screen_and_buy(self, bars: dict[str, BarData]):
        scores = []
        for vt_symbol, bar in bars.items():
            # 过滤逻辑：排除涨跌停（A股涨停通常无法买入）
            if bar.close_price >= bar.open_price * 1.098: 
                continue
            
            # 高开因子计算：(尾盘拉升幅度 * 成交量放大倍数)
            # 这里的逻辑是寻找尾盘有资金异常流入且维持强势的标的
            change = (bar.close_price - bar.open_price) / bar.open_price
            score = change * bar.volume
            scores.append((vt_symbol, score))
        
        # 排序并选取前5名
        selected = sorted(scores, key=lambda x: x[1], reverse=True)[:self.stock_count]
        
        for vt_symbol, score in selected:
            buy_price = bars[vt_symbol].close_price
            volume = int(self.capital_per_stock / buy_price / 100) * 100
            if volume > 0:
                self.buy(vt_symbol, buy_price, volume)
                self.active_stocks.append(vt_symbol)

    def sell_all_holdings(self, bars: dict[str, BarData]):
        """次日清仓逻辑"""
        for vt_symbol in list(self.active_stocks):
            if vt_symbol in bars:
                # 使用当前价卖出，由于是回测，cross_limit_order 会处理成交
                self.sell(vt_symbol, bars[vt_symbol].close_price, self.pos) 
                self.active_stocks.remove(vt_symbol)