---
layout: default
---

## Introduction to Pairs Trading

The primary goal in an investment endeavor is the implementation of strategies that minimise the risk while also maximising the finanical gain or return from said investment. While there have been many popular strategies and techniques developed over the years that point towards the same goal, the 'Pairs-Trading' strategy is one that has been used to great extent in modern hedge-funds, for its simplicity and inherent market-neutral qualities. This strategy, often termed a statistical-arbitrage, relies on monitoring the correlation between a pair of stocks (known to be correlated). A long position is opened on the stock that rises and a short position is opened on the stock that falls. The underlying assumption in pairs-trading is that pairs of stocks, that have historically shown similarities in their behavior will eventually converge in the long run, even if they diverge in the short term, allowing the trader to profit off the pair regardless of the market. 

In such a strategy, identification of correlated stocks and generation of pairs is of paramount importance. In this project, we employ unsupervised learning techniques that include Desnity Based Spatial Cluster of Applications with Noise and K-Means Algorithm. Once, the relevant pairs have been identified, their price relations are extrapolated using supervised learning techniques such as Linear Regression. This overall methodoldogy will help provide insight into the relations between various stocks and facilate the generation of appropriate trading strategies for them.  

## Dataset and Preprocessing

The datasets are provided by Wharton Research Data Services (WRDS). We mainly obtained the daily stock files from file from CRSP and quarterly fundamentals from Compustats for our purpose. Initially, our dataset consists stock price files from 3000 stocks which are constituents of Russell 3000. Those stocks' value and size are large enough to restore the whole market value, representing approximately 95% of the total market shares. We performed this pre-screening process to avoid the 'small-cap' trap in the market. Currently there are more than 6000 active stocks in the U.S. Stock Market but most of them are micro-valued. In reality, investors often cautiously avoid investing in those stocks, since trading even a small number of shares might has unpredictable effects on their stock prices. We should keep this in mind when doing acedamic research. We set the sample period from 2010-01-01 to 2015-12-31 for training strategies and use sample period 2016-01-01 to 2019-12-31 tfor backtesting. 

In our next stage, we want to pre-select eligible stocks which enable us sail through further steps. First we removed stocks that was dilisted, exchanged or merged during our sample period since those stocks are no longer tradable. Next we removed stocks that have negative price which will be problematic for further analysis. Stocks that are constantly trading at-low-volume also have to be removed since improper trading executions can largely change their stock prices and altered the history. Finally, we remove stocks that have more than half missing prices. Similar approach was performed to the financial fundamentals datasets. In the end, there are 1795 eligible stocks for further analysis. 

## Principal Component Analysis and Clustering Analysis


## Trading Strategy

In this section, we will discuss how we generate the z-score history by stock pair's price history. We generate the z-score history to decide when we long and short the stocks. The z-score is simply (spread)/(standard deviation of spread) and spread is calculated based on the stock pair's price history. The basic method to calculate the spread is using a log of prices of stocks A and B.
Spread = log(a) - nlog(b), where 'a' and 'b' are prices of stocks A and B respectively. The 'n' is the hedge ratio which is constant.
Calculate 'n' using regression so that spread is as close to 0 as possible. Also, since stocks A and B are cointegrated, the spread tends to converge to 0. To calculate the spread, we used the polynomial linear regression and linear regression with the Kalman filter. The data used to calculate the spread is the history of the stocks' prices for the previous 700 days. 

### Lnear Regression
We used the log of stock A's prices as data points and the log of stock B's prices as a label. We train the model with these datasets. After we generate the model, we predict the log(b) and calculate the spread as:

Spread = lr.pred(log(a)) - log(b)

It also leads us to calculate the z-score by the following equation:

z-score = Spread / standard deviation

The standard deviation is calculated by training data, which is the previous 700 days of prices' spread history.
We also used the degree = 4 for the polynomial linear regression hyperparameter. If it becomes too big, it goes to overfitting and will not generate the spread. If the spread distribution is small, it is hard to decide when we long and short the stocks. Here is the example graph of z-score history for the stock pairs we have. You can see it converges.

![z-score](https://github.com/daehkim/pair-trading/blob/master/pictures/each_pair_z_score.png)

### Linear Regression with Kalman Filter
(Zhenyu Jia)

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](https://guides.github.com/activities/hello-world/branching.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>

```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```


```
The final element.
```

## Contribution
- Daehyun Kim
  - Trading Strategy Structure
  - Trading Strategy Algorithm (Linear Regression)
  - Backtesting

## Reference
https://blog.quantinsti.com/pairs-trading-basics/

https://en.wikipedia.org/wiki/Pairs_trade
