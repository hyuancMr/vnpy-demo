from vnpy.event import EventEngine

from vnpy.trader.engine import MainEngine
from vnpy_ctastrategy import CtaStrategyApp, CtaEngine
from vnpy_ctabacktester import CtaBacktesterApp, BacktesterEngine
from vnpy_datamanager import DataManagerApp
from datetime import datetime


def main():
    event_engine = EventEngine()

    main_engine = MainEngine(event_engine)

    # main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(DataManagerApp)

    # cta_engine:CtaEngine = main_engine.get_engine("CtaStrategy")
    # cta_engine.init_engine()
    # cta_engine.init_all_strategies()

    backtester_engine:BacktesterEngine = main_engine.get_engine("CtaBacktester")
    # backtester_engine.start_downloading(
    #   "601212.SSE",
    #   "d",
    #   datetime(2025, 1, 1),
    #   datetime(2026, 1, 1)
    # )
    backtester_engine.init_engine()
    backtester_engine.start_backtesting(
      class_name="TestStrategy",
      vt_symbol="601212.SSE",
      interval="tick",
      start=datetime(2025, 1, 1),
      end=datetime(2025, 1, 2),
      rate="0.000025",
      slippage="0.2",
      size="300",
      pricetick="0.2",
      capital="1000000",
      setting={}
    )

if __name__ == "__main__":
    main()
