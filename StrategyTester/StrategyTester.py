import pandas as pd
from example_strategy import FVGStrategy
from tqdm import tqdm

class StrategyTester:
    def __init__(self, strategy_data, raw_data, initial_balance=10000):
        self.strategy_data = strategy_data.copy()
        self.raw_data = raw_data.copy()
        self.initial_balance = initial_balance
        self.balance = initial_balance

    def win_rate(self):
        winning_trades = 0
        total_trades = 0

        for index, row in tqdm(self.strategy_data.iterrows()):
            if row['Trade Type'] == 'Buy':
                total_trades += 1
                subsequent_data = self.raw_data.loc[index:]
                for _, s_row in subsequent_data.iterrows():
                    if s_row['High'] >= row['Take Profit']:
                        winning_trades += 1
                        break
                    elif s_row['Low'] <= row['Stop Loss']:
                        break

            elif row['Trade Type'] == 'Sell':
                total_trades += 1
                subsequent_data = self.raw_data.loc[index:]
                for _, s_row in subsequent_data.iterrows():
                    if s_row['Low'] <= row['Take Profit']:
                        winning_trades += 1
                        break
                    elif s_row['High'] >= row['Stop Loss']:
                        break

        return (winning_trades / total_trades) * 100 if total_trades != 0 else 0
    
    def max_drawdown(self):
        # Calculate cumulative returns
        self.strategy_data['Cumulative Return'] = (1 + self.strategy_data['Return']).cumprod()
        # Calculate the running maximum
        self.strategy_data['Running Max'] = self.strategy_data['Cumulative Return'].cummax()
        # Calculate drawdown
        self.strategy_data['Drawdown'] = (self.strategy_data['Running Max'] - self.strategy_data['Cumulative Return']) / self.strategy_data['Running Max']
        
        return self.strategy_data['Drawdown'].max()
    
    def sharpe_ratio(self, risk_free_rate=0.0):
        # Assuming daily data, to annualize: sqrt(252) is used as a common factor for daily trading data
        trading_days = 252
        avg_return = self.strategy_data['Return'].mean() * trading_days
        return_std = self.strategy_data['Return'].std() * np.sqrt(trading_days)
        
        return (avg_return - risk_free_rate) / return_std
    
    def evaluate(self):
        metrics = {
            "Win Rate": self.win_rate(),
            # "Maximum Drawdown": self.max_drawdown(),
            # "Sharpe Ratio": self.sharpe_ratio()
        }
        return metrics
    
# Load the newly provided dataset
dataset_new = pd.read_excel("./Data/HISTDATA_COM_XLSX_EURUSD_M12020/DAT_XLSX_EURUSD_M1_2020.xlsx")

# Adjusting the column names
dataset_new.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
dataset_new = dataset_new.iloc[1:]  # Drop the first row as it's now redundant

# Adjust the datatype of the Timestamp column
dataset_new['Timestamp'] = pd.to_datetime(dataset_new['Timestamp'])

# Instantiate the class and apply the strategy
strategy = FVGStrategy(dataset_new)
result_data = strategy.apply_strategy()

# Instantiate the StrategyTester class and evaluate the strategy
tester = StrategyTester(result_data, dataset_new)
strategy_metrics = tester.evaluate()
print(strategy_metrics)
