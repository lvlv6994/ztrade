import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime, timedelta

class StockSelector:
    def __init__(self, ts_token):
        """初始化选股器"""
        ts.set_token(ts_token)
        self.pro = ts.pro_api()
        
    def get_basic_info(self):
        """获取所有A股基本信息"""
        try:
            # 获取所有上市公司基本信息
            df = self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,name,industry,market,list_date'
            )
            return df
        except Exception as e:
            print(f"获取基本信息失败: {str(e)}")
            return None

    def get_financial_indicators(self, ts_code):
        """获取财务指标"""
        try:
            # 获取最新一期的财务指标
            df = self.pro.financial_indicator(
                ts_code=ts_code,
                start_date=(datetime.now() - timedelta(days=365)).strftime('%Y%m%d'),
                end_date=datetime.now().strftime('%Y%m%d')
            )
            return df.iloc[0] if not df.empty else None
        except Exception as e:
            print(f"获取财务指标失败: {str(e)}")
            return None

    def get_daily_indicators(self, ts_code):
        """获取每日指标"""
        try:
            # 获取最近30天的每日指标
            df = self.pro.daily_basic(
                ts_code=ts_code,
                start_date=(datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
                end_date=datetime.now().strftime('%Y%m%d')
            )
            return df.iloc[0] if not df.empty else None
        except Exception as e:
            print(f"获取每日指标失败: {str(e)}")
            return None

    def select_stocks(self, max_stocks=10):
        """选股主函数"""
        selected_stocks = []
        
        # 获取基本面信息
        basic_df = self.get_basic_info()
        if basic_df is None:
            return pd.DataFrame()

        # 筛选条件
        for _, stock in basic_df.iterrows():
            try:
                # 获取财务指标
                fin_data = self.get_financial_indicators(stock['ts_code'])
                if fin_data is None:
                    continue

                # 获取每日指标
                daily_data = self.get_daily_indicators(stock['ts_code'])
                if daily_data is None:
                    continue

                # 应用选股条件
                if self._apply_filters(stock, fin_data, daily_data):
                    selected_stocks.append({
                        'ts_code': stock['ts_code'],
                        'name': stock['name'],
                        'industry': stock['industry'],
                        'pe': daily_data['pe'],
                        'pb': daily_data['pb'],
                        'roe': fin_data['roe']
                    })

                if len(selected_stocks) >= max_stocks:
                    break

            except Exception as e:
                print(f"处理股票 {stock['ts_code']} 时出错: {str(e)}")
                continue

        return pd.DataFrame(selected_stocks)

    def _apply_filters(self, stock, fin_data, daily_data):
        """应用选股条件"""
        try:
            # 1. 市盈率(PE)过滤
            if daily_data['pe'] <= 0 or daily_data['pe'] > 50:
                return False

            # 2. 市净率(PB)过滤
            if daily_data['pb'] <= 0 or daily_data['pb'] > 5:
                return False

            # 3. ROE过滤
            if fin_data['roe'] <= 8:
                return False

            # 4. 总市值过滤（单位：亿元）
            if daily_data['total_mv'] < 50 or daily_data['total_mv'] > 3000:
                return False

            # 5. 排除ST股票
            if 'ST' in stock['name']:
                return False

            return True

        except Exception as e:
            print(f"应用过滤条件时出错: {str(e)}")
            return False
