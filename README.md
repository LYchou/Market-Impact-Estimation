# Project Description

When conducting factor investing and scaling up investments, market impact needs to be considered. Small-cap stocks are typically less efficient and contain many alpha opportunities, but due to their lack of liquidity, they might lead to a situation where profits are theoretically high but practically unattainable. This means that while backtest performance may be excellent, it can be difficult to profit in actual trading due to significant market impact. Therefore, estimating market impact during backtesting helps to discern which returns are realistically achievable.

Typically, backtests and strategy development assume trading at the opening price. However, for most stocks, opening volume accounts for only a small fraction of the daily trading volume (on average about 1%, with a median of about 0.8%). Even with a modest fund size, liquidity issues can arise for S&P 500 constituents. Since I have only obtained Level 1 data for a subset of stocks (U.S. stocks as of May 2024) with only trade data for each tick, I used the first trade of the opening to capture the opening volume.

Obtaining daily stock trading volume is much cheaper than obtaining opening volume (which requires tick data). Therefore, the purpose of this study is to estimate the "opening volume as a percentage of total daily volume" using daily data.

This way, both in backtests and actual trading, we can better understand market impact.

Although we do not have Level 2 data, understanding the "opening volume as a percentage of total daily volume" can still give a rough idea of market impact. For example, when backtesting historical data, if we know the opening trading amount for the day, we can calculate the proportion of our trades to the opening trading amount:
- 1%: No impact
- 20%: Pushes up by 1 tick
- 50%: Pushes up by 10 ticks

These estimates will help to more accurately measure market impact and adjust strategies in actual operations.

## Conclusion

In this study, we explored the factors affecting the proportion of opening volume to total daily volume (ov2tv) and concluded the following through multiple regression analysis:

### Impact Directions of Variables

1. **The larger the market cap of the stock, the larger the current ov2tv**:
   Larger market cap stocks generally attract more attention from investors, leading to higher trading volumes at the opening, reflecting the market's quick response to new information.
   Small-cap stocks not only have limited capital capacity but also have a lower proportion of opening volume to total daily volume, indicating a slower market response to these stocks.

2. **The larger the absolute value of the closing return from two days ago to one day ago, the larger the current ov2tv**:
   When there is significant price fluctuation in the previous day, investors tend to trade more actively at the opening to respond to these fluctuations.

3. **The larger the absolute value of the closing return from one day ago to today, the larger the current ov2tv**:
   When there is significant fluctuation in the previous day, investors trade more frequently at the opening to capture new market opportunities.

4. **The higher the turnover rate from the previous day, the larger the current ov2tv**:
   A high turnover rate in the previous day indicates high market activity for the stock, which usually carries over into the opening trades of the current day.

5. **The higher the turnover rate for the current day, the smaller the current ov2tv**:
   A high turnover rate for the current day reflects high activity throughout the day, meaning trading activity is spread throughout the day rather than concentrated at the opening.

These conclusions indicate that understanding the factors affecting ov2tv helps to better grasp market impact and make more accurate strategy adjustments in actual trading. Knowing these variables can help to more accurately estimate market impact in both backtests and live trading, thereby improving the effectiveness of strategy implementation.

## Data Description

- `data/open_trade.xlsx`: Official Open (exchange official opening trade) including price and volume
- `data/db/c2c_ret.xlsx`: Close-to-close returns (adjusted for dividends)
- `data/db/o2o_ret.xlsx`: Open-to-open returns (adjusted for dividends)
- `data/db/close.xlsx`: Closing prices
- `data/db/open.xlsx`: Opening prices
- `data/db/volume.xlsx`: Trading volume
- `data/db/shares_outstanding.xlsx`: Shares outstanding
- `data/db/univ`: Whether the stock is included in the S&P 500 index on the given day (boolean)

## Preliminary Data Analysis

### Opening Volume / Total Daily Volume

1. Calculate statistics (mean, std, min, 25%, 50%, 75%, max) over time for more than 500 stocks.
2. Take the median of the above statistics for the stock direction.

```plaintext
mean      0.010214
std       0.005347
min       0.003715
25%       0.007005
50%       0.008930
75%       0.011757
max       0.026999
```

We find that the mean (opening volume / total daily volume) is approximately 1.02%, and the median (opening volume / total daily volume) is approximately 0.89%. Therefore, the proportion of opening volume to total daily volume is not high.

### Opening Trading Amount = Opening Volume * Opening Price

1. Obtain the opening trading amount for S&P 500 constituents.
2. Calculate the average over time.
3. Sort.

```plaintext
ticker
ONL     2.694309e+04
ZIMV    4.868891e+04
EMBC    7.331892e+04
FOX     1.163689e+05
LUMN    1.182406e+05
            ...     
META    7.984950e+07
AMZN    1.097567e+08
MSFT    1.176218e+08
AAPL    1.614234e+08
NVDA    3.060501e+08
Length: 526
```

We find that the stocks with the largest opening trading volume are primarily the seven tech giants. Conversely, the stocks with the least trading volume are very few. For a small fund with AUM = 1,000,000, if we select 50 stocks equally weighted, the amount to be bought for each stock is 1,000,000 / 50 = 50,000 = 5+e04.

For stocks like NVDA, AAPL, MSFT, there will be almost no market impact. But for stocks like ONL, ZIMV, EMBC, if we simulate buying all at the opening as in the backtest, there will be significant market impact (the buying amount is roughly equal to the opening trading amount).

## Research Objective

We hope to find a good estimation formula using the data from May 2024.

Definitions:
- `ov2to` = Opening volume / Total daily volume
- `mktc` = Closing price * Shares outstanding
- `trv` = Total daily volume / Shares outstanding
- `retabs` = Absolute value of close-to-close daily returns

Construct the regression formula:
`ov2to = f(mktc_lag, retabs_lag, trv_lag, retabs, trv)`

```plaintext
             OLS Regression Results                            
==============================================================================
Dep. Variable:                  ov2tv   R-squared:                       0.142
Model:                            OLS   Adj. R-squared:                  0.141
Method:                 Least Squares   F-statistic:                     348.8
Date:                Fri, 19 Jul 2024   Prob (F-statistic):               0.00
Time:                        18:45:05   Log-Likelihood:                 37888.
No. Observations:               10562   AIC:                        -7.576e+04
Df Residuals:                   10556   BIC:                        -7.572e+04
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
----------------------------------------------------------------------------------
const              0.0108   6.52e-05    166.380      0.000       0.011       0.011
mktc_lag           0.0015   7.34e-05     19.884      0.000       0.001       0.002
c2c_absret_lag     0.0003   7.41e-05      3.959      0.000       0.000       0.000
c2c_absret         0.0002   7.44e-05      3.264      0.001    9.71e-05       0.000
trv_lag            0.0014      0.000     10.178      0.000       0.001       0.002
trv               -0.0030      0.000    -21.752      0.000      -0.003      -0.003
==============================================================================
Omnibus:                     8643.369   Durbin-Watson:                   1.263
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           369307.497
Skew:                           3.649   Prob(JB):                         0.00
Kurtosis:                      31.034   Cond.

 No.                         4.53
==============================================================================
Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
