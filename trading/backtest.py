from trader import AStockTrader
from strategy import MAStrategy

class Backtest:
    def __init__(self, trader:AStockTrader, strategy:MAStrategy):
        self.trader = trader
        self.strategy = strategy
        self.positions = {}
        self.cash = 1000000
        self.trade_history = []

    def run(self, code, start_date, end_date):
        """运行回测"""
        # 获取数据
        df = self.trader.get_daily_data(code, start_date, end_date)
        
        # 生成信号
        df = self.strategy.generate_signals(df)
        
        # 模拟交易
        for index, row in df.iterrows():
            if row['signal'] == 1 and code not in self.positions:
                # 买入
                shares = self.cash // (row['close'] * 100) * 100  # 买入股数（按手交易）
                cost = shares * row['close']
                if cost <= self.cash:
                    self.positions[code] = shares
                    self.cash -= cost
                    self.trade_history.append({
                        'date': row['trade_date'],
                        'action': 'buy',
                        'price': row['close'],
                        'shares': shares
                    })
            
            elif row['signal'] == -1 and code in self.positions:
                # 卖出
                shares = self.positions[code]
                self.cash += shares * row['close']
                del self.positions[code]
                self.trade_history.append({
                    'date': row['trade_date'],
                    'action': 'sell',
                    'price': row['close'],
                    'shares': shares
                })
