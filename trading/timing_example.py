import tushare as ts
from datetime import datetime, timedelta
from timing_strategy import TimingStrategy
from settings import Constant
# 初始化
ts.set_token(Constant.TUSHARE_TOKEN)
pro = ts.pro_api()

# 创建策略实例
strategy = TimingStrategy(
    rsi_period=14,
    rsi_buy_threshold=30,
    rsi_sell_threshold=70
)

# 获取股票数据
def get_stock_data(code, days=60):
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    df = pro.daily(ts_code=code, 
                   start_date=start_date,
                   end_date=end_date)
    
    return df.sort_values('trade_date')

# 获取数据并执行策略
code = "000001.SZ"  # 平安银行
df = get_stock_data(code)

# 获取策略建议
suggestion = strategy.get_position_suggestions(df)

if suggestion:
    print(f"\n策略建议：")
    print(f"操作方向：{suggestion['action']}")
    print(f"原因：{suggestion['reason']}")
    print(f"\n指标详情：")
    print(f"RSI：{suggestion['rsi']:.2f}")
    print(f"MACD柱状图：{suggestion['macd_hist']:.4f}")
    print(f"布林带位置：{suggestion['bb_position']:.2f}")
