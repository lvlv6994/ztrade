class HighFrequencyTrader:
    def __init__(self, initial_capital=50000, profit_target=0.02, stop_loss=0.01):  # 5万初始资金
        self.capital = initial_capital
        self.positions = {}
        self.trade_history = []
        self.current_price = None
        self.entry_price = None
        self.strategy = {
            'profit_target': profit_target,  # 2%的目标利润
            'stop_loss': stop_loss      # 1%的止损线
        }
        
    def check_exit_signals(self, current_price):
        """检查是否需要平仓"""
        if not self.entry_price:
            return False
            
        profit_ratio = (current_price - self.entry_price) / self.entry_price
        
        # 达到目标利润或触及止损线
        if profit_ratio >= self.strategy.get('profit_target') or self.strategy.get('stop_loss') > profit_ratio:
            return True
        return False
        
    def execute_trade(self, signal, price, volume, timestamp):
        """执行交易"""
        if signal == 1 and not self.positions:  # 开仓
            # 计算可买入数量（考虑手续费）
            available_capital = self.capital * 0.95  # 预留5%作为手续费缓冲
            shares = (available_capital // (price * 100)) * 100  # 确保整手交易
            cost = shares * price * (1 + 0.00025)  # 考虑万分之2.5的手续费
            
            if cost <= self.capital:
                self.positions['shares'] = shares
                self.capital -= cost
                self.entry_price = price
                self.trade_history.append({
                    'timestamp': timestamp,
                    'action': 'buy',
                    'price': price,
                    'shares': shares,
                    'cost': cost
                })
                
        elif (signal == -1 or self.check_exit_signals(price)) and self.positions:  # 平仓
            shares = self.positions['shares']
            revenue = shares * price * (1 - 0.00025 - 0.001)  # 考虑手续费和印花税
            self.capital += revenue
            self.positions = {}
            self.entry_price = None
            self.trade_history.append({
                'timestamp': timestamp,
                'action': 'sell',
                'price': price,
                'shares': shares,
                'revenue': revenue
            }) 
