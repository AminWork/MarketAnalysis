import pandas as pd

class FVGStrategy:
    def __init__(self, data):
        self.data = data.copy()
        self.data['FVG_Type'] = 'None'
        self.data['Trade Type'] = 'None'
        self.data['Entry'] = None
        self.data['Stop Loss'] = None
        self.data['Take Profit'] = None
    
    def detect_FVGs(self):
        # BISI Mode
        bisi_condition = (self.data['Low'].shift(-2) > self.data['High'])
        self.data.loc[bisi_condition, 'FVG_Type'] = 'BISI'
        
        # SIBI Mode
        sibi_condition = (self.data['High'].shift(-2) < self.data['Low'])
        self.data.loc[sibi_condition, 'FVG_Type'] = 'SIBI'
        
        # Drop rows where FVG_Type is 'None'
        self.data = self.data[self.data['FVG_Type'] != 'None']
    
    def generate_signals(self):
        # BISI Signals
        bisi_rows = self.data[self.data['FVG_Type'] == 'BISI'].index
        for idx in bisi_rows:
            if idx + 3 in self.data.index:
                self.data.at[idx+3, 'Trade Type'] = 'Buy'
                self.data.at[idx+3, 'Entry'] = self.data.at[idx+3, 'Open']
                self.data.at[idx+3, 'Stop Loss'] = min(self.data.loc[idx:idx+2, 'Low'])
                self.data.at[idx+3, 'Take Profit'] = self.data.at[idx+3, 'Entry'] + 2 * (self.data.at[idx+3, 'Entry'] - self.data.at[idx+3, 'Stop Loss'])
        
        # SIBI Signals
        sibi_rows = self.data[self.data['FVG_Type'] == 'SIBI'].index
        for idx in sibi_rows:
            if idx + 3 in self.data.index:
                self.data.at[idx+3, 'Trade Type'] = 'Sell'
                self.data.at[idx+3, 'Entry'] = self.data.at[idx+3, 'Open']
                self.data.at[idx+3, 'Stop Loss'] = max(self.data.loc[idx:idx+2, 'High'])
                self.data.at[idx+3, 'Take Profit'] = self.data.at[idx+3, 'Entry'] - 2 * (self.data.at[idx+3, 'Stop Loss'] - self.data.at[idx+3, 'Entry'])

    def apply_strategy(self):
        self.detect_FVGs()
        self.generate_signals()
        return self.data
