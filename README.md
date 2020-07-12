---
layout: default
---

## Introduction to Pairs Trading

The primary goal in an investment endeavor is the implementation of strategies that minimize the risk while also maximizing the financial gain or return from the said investment. While there have been many popular strategies and techniques developed over the years that point towards the same goal, the 'Pairs-Trading' strategy is one that has been used to great extent in modern hedge-funds, for its simplicity and inherent market-neutral qualities. This strategy, often termed a statistical-arbitrage, relies on monitoring the correlation between a pair of stocks (known to be correlated). A long position is opened on the stock that rises and a short position is opened on the stock that falls. The underlying assumption in pairs-trading is that pairs of stocks, that have historically shown similarities in their behavior will eventually converge in the long run, even if they diverge in the short term, allowing the trader to profit off the pair regardless of the market. 

In such a strategy, identification of correlated stocks and generation of pairs is of paramount importance. In this project, we employ unsupervised learning techniques that include Density-Based Spatial Cluster of Applications with Noise and K-Means Algorithm. Once, the relevant pairs have been identified, their price relations are extrapolated using supervised learning techniques such as Linear Regression. This overall methodology will help provide insight into the relations between various stocks and facilitate the generation of appropriate trading strategies for them.  

## Dataset and Preprocessing

The datasets are provided by Wharton Research Data Services (WRDS). We mainly obtained the daily stock files from file from CRSP and quarterly fundamentals from Compustats for our purpose. Initially, our dataset consists of stock price files from 3000 stocks which are constituents of Russell 3000. Those stocks' value and size are large enough to restore the whole market value, representing approximately 95% of the total market shares. We performed this pre-screening process to avoid the 'small-cap' trap in the market. Currently, there are more than 6000 active stocks in the U.S. Stock Market but most of them are micro-valued. In reality, investors often cautiously avoid investing in those stocks, since trading, even a small number of shares might have unpredictable effects on their stock prices. We should keep this in mind when doing academic research. We set the sample period from 2010-01-01 to 2015-12-31 for training strategies and use sample period 2016-01-01 to 2019-12-31 for backtesting. 

In our next stage, we want to pre-select eligible stocks that enable us to sail through further steps. First, we removed stocks that were delisted, exchanged, or merged during our sample period since those stocks are no longer tradable. Next, we removed stocks that have negative prices which will be problematic for further analysis. Stocks that are constantly trading at-low-volume also have to be removed since improper trading executions can largely change their stock prices and altered history. Finally, we remove stocks that have more than half missing prices. A similar approach was performed on the financial fundamentals of datasets. In the end, there are 1795 eligible stocks for further analysis. 

## Principal Component Analysis and Clustering Analysis

### Principal Component Analysis


Two clustering algorithms were explored to create clusters of stocks. It is to be noted here that during clustering, each individual stock price data and each individual financial ratios were considered independant features and clustering was done based on the entire set of features as a whole. 
### Density-based spatial clustering of applications with Noise
The DBSCAN algorithm was paramterized by eps = 1.8 and minPoints = 3 which resulted in the formation of 11 clusters. A simple visualization of the cluster in the form of a T-SNE plot is shown below:
![T-SNE plot for DBSCAN](https://github.com/daehkim/pair-trading/blob/master/pictures/DBSCAN_plots/T-SNE_plot_for_stock_clusters.png)
The following figure shows the number of members in each cluster, demontrating the fact that a huge proportion of the stocks are bunched into a single cluster. This disproportionate distribution of the stocks in clusters is expected to some extent, since the dataset is possibly dominated by stocks from a single or closely related industries.
![Cluster Member counts for DBSCAN](https://github.com/daehkim/pair-trading/blob/master/pictures/DBSCAN_plots/cluster_member_counts.png)

In order to increase confidence in the clustering procedure, the real time series stock price data of the stocks in each cluster were also investigated. The time series data of the stocks in 4 of the 11 clusters are illustrated below. From a visual perspective, stocks within the same cluster do show a realtively high correlation among them in terms of the behavior of the stock prices. 
![Stock price in each cluster](https://github.com/daehkim/pair-trading/blob/master/pictures/DBSCAN_plots/combined_time_Series.png)

### KMeans Clustering
The KMeans clustering algorithm is a popular clustering methodolgy employed in pair-trading implementeations. The most important aspect of this algorithm is the determination of the number of clusters. This can be ascertained using an elbow-method based cross-validation technique. There are three loss-metrics (or scores) that can be used in the elbow method which are: 

1) Distortion Score:
2) Silhouette Score:
3) Calinski Harabz Score:

The elbow for each of the above mentioned score is illustrated below. An average of the elbow from each of these independant metrics was finally used in training the KMeans Algorithm. 

Therefore, the Kmeans clustering was finally implemented by pre-defining the number of clusters to be 14. The following plot shows a visualization of the clustered datapoints in the form of a T-SNE plot. Again, similar to what was observed with DBSCAN, we notice a slight disproportionality in the size of each cluster, which as mentioned before, can be expected. 
![Cluster Member counts for DBSCAN](https://github.com/daehkim/pair-trading/blob/master/pictures/Kmeans_plots/T_SNE_kmeans.png)

## Trading Strategy

In this section, we will discuss how we generate the z-score history by stock pair's price history. We generate the z-score history to decide when we long and short the stocks. The z-score is simply (spread)/(standard deviation of spread) and spread is calculated based on the stock pair's price history. The basic method to calculate the spread is using a log of prices of stocks A and B.
Spread = log(a) - nlog(b), where 'a' and 'b' are prices of stocks A and B respectively. The 'n' is the hedge ratio which is constant.
Calculate 'n' using regression so that spread is as close to 0 as possible. Also, since stocks A and B are cointegrated, the spread tends to converge to 0. To calculate the spread, we used the polynomial linear regression and linear regression with the Kalman filter. The data used to calculate the spread is the history of the stocks' prices for the previous 700 days. 

### Lnear Regression

We used the log of stock A's prices as data points and the log of stock B's prices as a label. We train the model with these datasets. After we generate the model, we predict the log(b) and calculate the spread as:

Spread = lr.pred(log(a)) - log(b)

It also leads us to calculate the z-score by the following equation:

z-score = Spread / standard deviation

The standard deviation is calculated by training data, which is the training data prices' spread history.
We also used the degree = 4 for the polynomial linear regression hyperparameter. If it becomes too big, it goes to overfitting and will not generate the spread. If the spread distribution is small, it is hard to decide when we long and short the stocks. Here is the example graph of z-score history for the stock pairs we have. You can see it converges.

![z-score](https://github.com/daehkim/pair-trading/blob/master/pictures/each_pair_z_score.png)

### Linear Regression with Kalman Filter
(Zhenyu Jia)

## Backtesting

In this section, we will discuss testing. We apply our trading strategy to the real stock market and check how much we can earn based on our approach. We used the moving windows approach for the testing. For the training data, we used the previous 700 days stock prices. After we train the model with our machine learning algorithm, we calculate the z-score with the generated model and decide whether we will long or short the stocks. The input of backtesting is the z-score history generated in the 'trading strategy' part and the price history. Based on the input, we keep calculating the earning and loss of our stock and inverse. We also track the total asset history and return it as an output of backtesting.

### Implementation

To simplify the backtesting, we just set the initial money as million dollars and the volume of the stocks we trading as 'total assets' / '# of pairs'. Therefore, if our current total asset is $100 and the number of stock pairs is 10, we long/short the stock only with $10. We also calculate the price of the inverse (short) in the everyday base and we didn't consider the commission of trading to simplify.

### Results

We run the backtesting for all the timeline (2007~2015). Here are all the results from the backtesting. The x-label is the daily based time. It does not include market off-day. The y-label is the money (dollars).

#### Each pair's assets

![each assets](https://github.com/daehkim/pair-trading/blob/master/pictures/each_pair_assets.png)

#### Total assets

![total assets](https://github.com/daehkim/pair-trading/blob/master/pictures/total_assets.png)


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
