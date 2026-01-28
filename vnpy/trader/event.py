"""
Event type string used in the trading platform.
定义交易平台中使用的事件类型字符串
"""

from vnpy.event import EVENT_TIMER  # noqa

# 行情 Tick 事件标识，对应交易标的的实时行情数据（如股票 / 期货的逐笔成交、盘口）
EVENT_TICK = "eTick."
# 成交事件标识，对应订单成交后的确认事件（记录成交价格、数量、方向等）
EVENT_TRADE = "eTrade."
# 订单事件标识，对应订单的状态变化（如委托、撤单、成交、拒单等）
EVENT_ORDER = "eOrder."
# 持仓事件标识，对应账户持仓的变化（如开仓、平仓后持仓量 / 方向变更）
EVENT_POSITION = "ePosition."
# 账户事件标识，对应账户资金变化（如入金、出金、手续费、盈亏导致的余额变更）
EVENT_ACCOUNT = "eAccount."
# 报价事件标识，通常对应做市商报价、期权报价等场景的事件
EVENT_QUOTE = "eQuote."
# 合约事件标识，对应交易合约信息的更新（如合约到期、参数调整、合约新增）
EVENT_CONTRACT = "eContract."
# 日志事件标识，对应系统运行日志的记录 / 推送（如错误日志、操作日志）
EVENT_LOG = "eLog"
