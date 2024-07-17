# Task

Calculate the trade performance of a given set of trades executed by a financial firm. The function take a pandas DataFrame as input with the following columns:
- Date (datetime64[ns]): The date and time of the trade
- Symbol (string): The ticker symbol of the traded security
- Side (string): Either 'buy' or 'sell'
- Size (float, optional): The number of shares traded (default to 1 if not provided)
- Price (float): The price at which the trade was executed

1. Choose 10 financial metrics for tracking trade performance of a strategy.
2. Account for both long and short strategies.
3. Use an auxiliary function:
```
def getTickerPrice(ticker: str, date: datetime64[ns]) -> float:
    # This function returns the price of the security 'ticker' at the given 'date'
    # For the purpose of this exercise, assume it returns a random number
    return random.uniform(1, 100)  # Example implementation
```
Use this function to get the current market price of securities when needed for your calculations.

## Definition of Terms
- **fillRatio**: the ratio of filled trades against total number of sent orders
- **sodPos**: initial position or start-of-day shares that one symbol owns
- **eodPos**: end-of-day shares that one symbol owns
- **fillSign**: sign of a trade, decided by “Side”. `buy` -> 1, `sell` -> -1
- **close**: last price or close auction price of a symbol when market is closed
- **preclose**: close price of the previous trading day
- **tpl**: trading PnL marked to close price, calculated by fillSign * Size * (close - Price)  
- **ntpl**: trading Pnl deducted by transaction costs or commission fee, calculated by tpl - fee
- **hpl**: holding Pnl, calculated by sodPos * (close - preclose) 
- **pnl**: total Pnl, calculated by tpl + hpl
- **markout**/return profile: trading PnL marked to a future reference price such as an arrival price, calculated by fillSign * Size * (ref_price - Price). Calculating difference time horizons can give us a pnl curve called return profile
- **gmv**: gross market value at the end of the day
- **nmv**: net market value at the end of the day, typically long market value - short market value
- **lmv**: long market value marked by close price
- **smv**: short market value marked by close price

## Assumptions
1. All trades are executed and fully filled (`fillRatio = 1`). Note that in production this would not happen all the time, so we generally need the records for all sent orders, not just executed trades. 
2. For simplicity, we assume the sodPos of first date is 0 for all symbols.   
3. For simplicity, we assume markets are opened on all weekdays, that is, all weekdays are trading dates.
4. Note that we can evalute the portfolio performance based on different horizon, such as on daily, weekly or monthly basis. The optimal monitoring metrics correspond to different observation horizons. For example, when dealing with a large universe (number of traded tickers), the daily monitoring metrics for production should focus on the fill ratio, trading volume, slippage, intraday PnL or return profile with different dimensions like trade side, symbol groups or time intervals. These indices reflect trading activities or any execution issue might happened in intraday production (also depend on the horizons of alpha or features of strategies). However, when monitoring over a period such as a week or a month, metrics like sharpe ratio, win rate, or max drawdown can be used to reflect the strategy's return and volatility. Here without any information on the strategy, for simplicity, I only give one summary table with general matrics across all days and all symbols for a given dataframe.
5. `getTickerPrice` function is lack of some illustrations. I’m not sure if it returns real-time prices or end-of-day prices. To avoid ambiguity and faciliate usage, I refined this function with a random number generator to return a dataframe with end-of-day closing prices for some given symbols and dates. The new function is `getClosePrice`.
6. For transaction cost or commission fee, we use **0.001** per share as an approximation.

## Performance Matrix:
Ten matrics selected to evaluate the performance of this strategy:
1. **tradeQty**: total number of shares for all filled trades
2. **tradeNotional**: Size* Price for all filled trades
3. **tpl_sum**: total trading Pnl for all symbols for all dates
4. **tpl_pt**: trading Pnl per trade, weighted by tradeNotional across dates
5. **ntpl_sum**: total net Pnl for all symbols for all dates
6. **gmv_avg**: average total market value across all dates
7. **nmv_avg**: average net market value across all dates
8. **sharpe**: a measure of risk-adjusted return
9. **winRate**: percentage of profitable dates
10. **maxDrawdown**: maximum observed loss from a peak to a trough.
    
The ouput table will also include information such as startDate, endDate, nTradingDate (counts of trading days), and nTradedSymbol (number of traded symbols).


