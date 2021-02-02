# BitMex_ANN_Trader
Python artificial network able to trade using BitMex API

The steps are the following:

- We already trained some artifical neural network on predicting trend of the Bitcoin for timeframe:
  - 15 minutes
  - 1 hour
  - 2 hours 
  - 4 hours

From delay ranging from 1 to 40. (but we will train again somme ann on more recent data, which could improve our results)


- Get necessary data in order to make a prediction on the ANN 
  - Pass by bitmex api to fetch last btc price 
  - Small difference between thoses prices and the one on which the training was performed due to Bitmex indexing, whoch transform a bit BTC price
  
- Once data is fetch, use it to compute the last RSI, Momentum and difference from moving average
  - Normalize all this, and pass it as input 

- Once the prediction is done: 
  - For the moment we will only back test, w/o picking any trade, to ensure of the accuracy of our ANN


