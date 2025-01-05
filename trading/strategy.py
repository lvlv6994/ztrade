class MAStrategy:
    """移动平均线策略"""
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        """生成交易信号
        当短期均线上穿长期均线时买入
        当短期均线下穿长期均线时卖出
        """
        df['MA_short'] = df['close'].rolling(self.short_window).mean()
        df['MA_long'] = df['close'].rolling(self.long_window).mean()
        
        df['signal'] = 0
        df.loc[df['MA_short'] > df['MA_long'], 'signal'] = 1  # 买入信号
        df.loc[df['MA_short'] < df['MA_long'], 'signal'] = -1  # 卖出信号
        
        return df
