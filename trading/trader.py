from datetime import datetime
import tushare as ts
import pandas as pd
import numpy as np

class AStockTrader:
    def __init__(self, token):
        # 初始化 tushare
        ts.set_token(token)
        self.pro = ts.pro_api()
        self.positions = {}  # 持仓
        self.cash = 1000000  # 初始资金 100万

    def get_daily_data(self, code, start_date, end_date):
        """获取股票日线数据"""
        df = self.pro.daily(ts_code=code, 
                           start_date=start_date, 
                           end_date=end_date)
        return df.sort_values('trade_date')
