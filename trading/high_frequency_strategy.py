class HighFrequencyStrategy:
    def __init__(self, 
                 volume_threshold=3.0,  # 成交量放大倍数阈值
                 price_change_threshold=0.02,  # 价格变动阈值 2%
                 profit_target=0.03,  # 目标利润 3%
                 stop_loss=0.015):    # 止损位 1.5%
        self.volume_threshold = volume_threshold
        self.price_change_threshold = price_change_threshold
        self.profit_target = profit_target
        self.stop_loss = stop_loss

    def calculate_indicators(self, df):
        """计算技术指标"""
        # 计算分钟K线的VWAP(成交量加权平均价格)
        df['vwap'] = (df['amount'] / df['volume']).fillna(df['close'])
        
        # 计算成交量的相对变化
        df['volume_ma5'] = df['volume'].rolling(5).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma5']
        
        # 计算价格变动率
        df['price_change'] = df['close'].pct_change()
        
        # 计算波动率 (ATR简化版)
        df['hl_range'] = df['high'] - df['low']
        df['volatility'] = df['hl_range'].rolling(5).mean()
        
        return df

    def generate_signals(self, df):
        """生成交易信号"""
        df = self.calculate_indicators(df)
        df['signal'] = 0
        
        # 买入条件：
        buy_conditions = (
            (df['volume_ratio'] > self.volume_threshold) &  # 成交量突然放大
            (df['price_change'] > 0) &  # 价格上涨
            (df['close'] > df['vwap'])  # 价格在VWAP上方
        )
        
        # 卖出条件：
        sell_conditions = (
            (df['price_change'] < -self.price_change_threshold) |  # 价格跌破阈值
            (df['close'] < df['vwap'])  # 价格跌破VWAP
        )
        
        df.loc[buy_conditions, 'signal'] = 1
        df.loc[sell_conditions, 'signal'] = -1
        
        return df 