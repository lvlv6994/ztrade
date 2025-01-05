from trader import AStockTrader
from strategy import MAStrategy
from backtest import Backtest

# 初始化
token = "24798a6230858ac2880a52dc5ea8e446a3fe531a3bdec6a5377c800c"  # 需要在tushare网站注册获取
trader = AStockTrader(token)
strategy = MAStrategy(short_window=5, long_window=20)
backtest = Backtest(trader, strategy)

# 运行回测
code = "000001.SZ"  # 平安银行
backtest.run(code, "20230101", "20231231")

# 查看交易历史
print(backtest.trade_history)
