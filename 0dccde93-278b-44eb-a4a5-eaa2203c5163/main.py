#Type code here//@version=4
strategy("Moving Averages Strategy for USOIL with Maxima and Minima", overlay=true)

// Define function for calculating simple moving average
sma_custom(src, length) =>
    sum = 0.0
    sum := nz(sum[1]) + src - nz(src[length])
    sum / length

// Calculate moving averages for each timeframe
ma_15min_50 = sma_custom(close, 50)

// Function to identify maxima and minima
isMinima(src, length) =>
    lowVal = lowest(src, length)
    src == lowVal

isMaxima(src, length) =>
    highVal = highest(src, length)
    src == highVal

// Check for minima and maxima conditions
minima_condition = isMinima(ma_15min_50, 50) and crossover(ma_15min_50, close)
maxima_condition = isMaxima(ma_15min_50, 50) and crossunder(ma_15min_50, close)

var inLongTrade = false
var inShortTrade = false

leverage = input(2, title="Leverage", minval=1, maxval=10)

// Calculate position size based on leverage
position_size = strategy.equity * leverage / close

if (minima_condition and not inLongTrade)
    inLongTrade := true
    inShortTrade := false
    strategy.entry("Buy", strategy.long, qty=position_size)

if (maxima_condition and not inShortTrade)
    inShortTrade := true
    inLongTrade := false
    strategy.entry("Sell", strategy.short, qty=position_size)

// Exit trades if opposite condition is met
exitCondition = (inLongTrade and maxima_condition) or (inShortTrade and minima_condition)
if (exitCondition)
    inLongTrade := false
    inShortTrade := false
    strategy.close("Buy")
    strategy.close("Sell")