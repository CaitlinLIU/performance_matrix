import pandas as pd
import numpy as np

class performanceMatrix(object):
    
    def __init__(self, data:pd.DataFrame):
            
        # Check if the DataFrame contains the required columns
        if not {'Date','Symbol','Side','Size','Price'}.issubset(data.columns):
            raise ValueError(f"The DataFrame does not contain the required columns")
        self.data = data
        self.symbols = data.Symbol.unique()
        self.dates = data.Date.unique()
    
    def showInputData(self):
        return self.data
    
    def getClosePrice(self):
        df1 = pd.DataFrame({'Date': self.dates})
        df2 = pd.DataFrame({'Symbol': self.symbols})
        df_close = df1.merge(df2, how='cross')
        df_close['close'] = np.random.uniform(1, 100, size=len(df_close))
        return df_close
    
    def calcStats(self) -> pd.Series:
        if self.data.empty:
            return None
        
        closePx = self.getClosePrice()
        data = self.data.merge(closePx, on=["Date","Symbol"], how="left")
        data['Size'] = data['Size'].fillna(1)
        data['fillSign'] = data['Side'].apply(lambda x: 1 if x == 'buy' else -1)
        data['SizeSigned'] = data['Size'] * data['fillSign']
        
        # trading related metrics
        data['tradeNotional'] = data['Size'] * data['Price']
        data['tpl'] = data['fillSign'] * data['Size'] * (data['close'] - data['Price'])
        data['tpl_pt'] = data['tpl'] / data['tradeNotional']
        data['ntpl'] = data['tpl'] - 0.001 * data['Size'] 
        # Aggregate to get daily trade volume
        daily_qty = data.groupby('Date').agg({'Size': 'sum', 'tradeNotional': 'sum'}).reset_index()
        
        # position related metrics
        data['pos'] = data.groupby(['Symbol'])['SizeSigned'].cumsum()
        positions = data.groupby(["Date", "Symbol"]).last().reset_index()
        positions['mv'] = positions['pos'] * positions['close']
        positions['lmv'] = positions.apply(lambda row: row['mv'] if row['pos'] > 0 else 0, axis=1)
        positions['smv'] = positions.apply(lambda row: abs(row['mv']) if row['pos'] < 0 else 0, axis=1)
        # Aggregate to get daily values
        daily_mv = positions.groupby('Date').agg({'lmv': 'sum', 'smv': 'sum'}).reset_index()
        
        # metrics across dates
        daily_returns = data.groupby('Date')['tpl'].sum()
        sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(len(daily_returns))
        win_rate = (daily_returns > 0).mean()
        cumulative_profit = daily_returns.cumsum()
        running_max = cumulative_profit.cummax()
        drawdown = running_max - cumulative_profit
        max_drawdown = drawdown.max()
        
        result = pd.Series({
            'startDate': data.Date.min().date(), 
            'endDate': data.Date.max().date(), 
            'nTradingDate': len(self.dates),
            'nTradedSymbol': len(self.symbols),
            'tradeQty_avg': daily_qty.Size.mean(), 
            'tradeNotional_avg': daily_qty.tradeNotional.mean(),
            'tpl_sum': data.tpl.sum(), 
            'ntpl_sum': data.ntpl.sum(),
            'tpl_pt': data.tpl.sum() / data.tradeNotional.sum(),
            'gmv_avg': np.mean(daily_mv['lmv'] + daily_mv['smv']),
            'nmv_avg': np.mean(daily_mv['lmv'] - daily_mv['smv']),
            'sharpe': sharpe_ratio, 
            'winRate': win_rate,
            'maxDrawdown': max_drawdown,
        })
        
        return result

if __name__ == "__main__":
        
    # Example usage
    data = pd.DataFrame({
        'Date': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02', '2024-01-02']),
        'Symbol': ['AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'AAPL'],
        'Side': ['buy', 'sell', 'sell', 'buy', 'sell'],
        'Size': [10, 5, 15, 20, 30],
        'Price': [150.0, 160.0, 200.0, 210.0, 170.0]
    })
    obj = performanceMatrix(data)
    # You can print the close price table here:
    print("This is input dataframe:")
    print(obj.showInputData())  
    print("\nThis is generated random price table:")
    print(obj.getClosePrice())  
    print("\nThis is output matrics:")
    print(obj.calcStats())  

