import pandas as pd
from datetime import datetime
from vnpy_ctastrategy.backtesting import BacktestingEngine
from vnpy.trader.constant import Interval, Exchange

# 导入你的策略类
from  vnpy_ctastrategy.strategies import TailTradeStrategy

def run_backtest(vt_symbol: str):
    """
    单个标的回测逻辑
    """
    engine = BacktestingEngine()
    
    # 设置回测参数
    engine.set_parameters(
        vt_symbol=vt_symbol,
        interval=Interval.MINUTE,
        start=datetime(2023, 1, 1),
        end=datetime(2023, 12, 31),
        rate=0.0003,      # A股佣金（万三）
        slippage=0.01,    # 假设1分钱滑点
        size=100,         # 1手=100股
        pricetick=0.01,   # 最小价格变动
        capital=100_000,  # 初始资金
    )
    
    # 添加策略
    engine.add_strategy(TailTradeStrategy, {})
    
    # 加载历史数据
    engine.load_data()
    
    # 执行回测
    engine.run_backtesting()
    
    # 计算统计指标
    engine.calculate_result()
    stats = engine.calculate_statistics(output=False) # 设置为False不打印冗长的每日明细
    
    return stats

if __name__ == "__main__":
    # 1. 模拟一个需要回测的股票列表 (实际应用中可以通过 tushare 获取)
    # 示例包含：主板 60/00, 剔除 300/688
    all_symbols = [
        "600036.SSE", "600519.SSE", "000001.SZSE", 
        "300059.SZSE", "688001.SSE" # 后面两个应该被策略内的过滤逻辑拦截或在此处手动排除
    ]
    
    results = []
    
    print("开始全A股（非创非科）批量回测...")
    
    for vt_symbol in all_symbols:
        # 手动二次过滤（保险起见）
        symbol = vt_symbol.split(".")[0]
        if symbol.startswith(("300", "688", "301")):
            print(f"跳过非主板标的: {vt_symbol}")
            continue
            
        print(f"正在回测: {vt_symbol}...")
        try:
            stats = run_backtest(vt_symbol)
            if stats:
                results.append({
                    "代码": vt_symbol,
                    "总收益率": stats["total_return"],
                    "胜率": stats["winning_rate"],
                    "盈亏比": stats["profit_loss_ratio"],
                    "成交笔数": stats["total_trade_count"]
                })
        except Exception as e:
            print(f"回测 {vt_symbol} 失败: {e}")

    # 2. 汇总结果展示
    if results:
        df = pd.DataFrame(results)
        # 按胜率从高到低排序
        df = df.sort_values(by="胜率", ascending=False)
        print("\n--- 回测结果汇总 ---")
        print(df)
        
        # 导出到Excel进一步分析
        # df.to_excel("backtest_results.xlsx", index=False)
    else:
        print("未获取到有效回测数据，请检查数据库中是否有对应历史Bar数据。")