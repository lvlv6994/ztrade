import pandas as pd
import numpy as np
import talib as ta

class TimingStrategy:
    def __init__(self, 
                 rsi_period=14,
                 rsi_buy_threshold=30,
                 rsi_sell_threshold=70,
                 macd_fast=12,
                 macd_slow=26,
                 macd_signal=9,
                 bb_period=20,
                 bb_std=2):
        """
        初始化择时策略参数
        
        参数:
            rsi_period (int): RSI计算周期
            rsi_buy_threshold (int): RSI买入阈值
            rsi_sell_threshold (int): RSI卖出阈值
            macd_fast (int): MACD快线周期
            macd_slow (int): MACD慢线周期
            macd_signal (int): MACD信号线周期
            bb_period (int): 布林带周期
            bb_std (int): 布林带标准差倍数
        """
        self.rsi_period = rsi_period
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.bb_period = bb_period
        self.bb_std = bb_std

    def calculate_indicators(self, df):
        """计算技术指标"""
        try:
            # 确保数据包含必要的列
            if 'close' not in df.columns:
                raise ValueError("数据中缺少'close'列")

            close_prices = df['close'].values

            # 计算RSI
            df['rsi'] = ta.RSI(close_prices, timeperiod=self.rsi_period)

            # 计算MACD
            macd, signal, hist = ta.MACD(close_prices, 
                                       fastperiod=self.macd_fast,
                                       slowperiod=self.macd_slow,
                                       signalperiod=self.macd_signal)
            df['macd'] = macd
            df['macd_signal'] = signal
            df['macd_hist'] = hist

            # 计算布林带
            df['bb_middle'], df['bb_upper'], df['bb_lower'] = ta.BBANDS(
                close_prices,
                timeperiod=self.bb_period,
                nbdevup=self.bb_std,
                nbdevdn=self.bb_std
            )

            return df

        except Exception as e:
            print(f"计算指标时出错: {str(e)}")
            return None

    def generate_signals(self, df):
        """生成交易信号"""
        try:
            df = self.calculate_indicators(df)
            if df is None:
                return None

            # 初始化信号列
            df['signal'] = 0

            # 生成买入信号 (1)
            buy_conditions = (
                (df['rsi'] < self.rsi_buy_threshold) &  # RSI超卖
                (df['macd_hist'] > 0) &  # MACD柱状图为正
                (df['close'] < df['bb_lower'])  # 价格低于布林带下轨
            )
            df.loc[buy_conditions, 'signal'] = 1

            # 生成卖出信号 (-1)
            sell_conditions = (
                (df['rsi'] > self.rsi_sell_threshold) |  # RSI超买
                (df['macd_hist'] < 0) |  # MACD柱状图为负
                (df['close'] > df['bb_upper'])  # 价格高于布林带上轨
            )
            df.loc[sell_conditions, 'signal'] = -1

            return df

        except Exception as e:
            print(f"生成信号时出错: {str(e)}")
            return None

    def get_position_suggestions(self, df):
        """获取持仓建议"""
        signals_df = self.generate_signals(df)
        if signals_df is None:
            return None

        latest_data = signals_df.iloc[-1]
        
        suggestion = {
            'signal': latest_data['signal'],
            'rsi': latest_data['rsi'],
            'macd_hist': latest_data['macd_hist'],
            'bb_position': (latest_data['close'] - latest_data['bb_middle']) / 
                         (latest_data['bb_upper'] - latest_data['bb_middle'])
        }

        if latest_data['signal'] == 1:
            suggestion['action'] = "买入"
            suggestion['reason'] = "RSI超卖，MACD柱状图转正，价格处于布林带下轨以下"
        elif latest_data['signal'] == -1:
            suggestion['action'] = "卖出"
            suggestion['reason'] = "RSI超买，MACD柱状图转负，价格处于布林带上轨以上"
        else:
            suggestion['action'] = "持观望"
            suggestion['reason'] = "无明确信号"

        return suggestion
