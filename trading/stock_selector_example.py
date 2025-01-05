from settings import Constant
from stock_selector import StockSelector
from pandas import DataFrame
# 初始化选股器
selector = StockSelector(Constant.TUSHARE_TOKEN)

# 获取推荐股票
selected_stocks:DataFrame = selector.select_stocks(max_stocks=10)

# 打印结果
if not selected_stocks.empty:
    print("\n选股结果：")
    print(selected_stocks.to_string(index=False))
else:
    print("未找到符合条件的股票")
