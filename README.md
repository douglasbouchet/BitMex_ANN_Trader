# HXRO_ANN_Trader
Python artificial network able to trade using the HXRO API

The steps are the following:

- We already trained some artifical neural network on predicting trend of the Bitcoin for timeframe 15 minute, delay {1 to 3} which correspond to the HXRO possibilities.


- Get necessary data in order to make a prediction on the ANN 
  - Cannot pass by bitmex cause data available only one day after
  - -> Pass by xhro api, where can get the BTC price in real time

  - Once data is fetch, use it to compute the last RSI, Momentum and difference from moving average
  - Normalize all this, and pass it as input 

- Once the prediction is done: 
  - Prediction says to open a trade -> use the HXRO api to "enter contest"

- While not actually picking trade on HXRO, make "fake trade", and compute the accuracy on them (+ PnL)

