import tushare as ts
from datetime import datetime, timedelta
from settings import Constant
from high_frequency_trader import HighFrequencyTrader
from high_frequency_strategy import HighFrequencyStrategy

# 初始化
ts.set_token(Constant.TUSHARE_TOKEN)
pro = ts.pro_api()

# 创建策略和交易器实例
strategy = HighFrequencyStrategy()
trader = HighFrequencyTrader(initial_capital=50000)

# 获取分钟级别数据
def get_minute_data(code, start_date, end_date):
    df = ts.pro_bar(ts_code=code, 
                    freq='1min',  # 1分钟K线
                    start_date=start_date,
                    end_date=end_date)
    return df

# 运行策略
code = "000001.SZ"  # 平安银行
start_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
end_date = datetime.now().strftime("%Y%m%d")

# 获取数据并执行策略
df = get_minute_data(code, start_date, end_date)
signals_df = strategy.generate_signals(df)

# 模拟交易
for index, row in signals_df.iterrows():
    trader.execute_trade(row['signal'], 
                        row['close'], 
                        row['volume'], 
                        row['trade_time'])

# 查看交易结果
print(f"最终资金: {trader.capital}")
print(f"交易次数: {len(trader.trade_history)}") 
