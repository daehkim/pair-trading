---
layout: default
---

## Introduction to Pairs Trading

The primary goal in an investment endeavor is the implementation of strategies that minimise the risk while also maximising the finanical gain or return from said investment. While there have been many popular strategies and techniques developed over the years that point towards the same goal, the 'Pairs-Trading' strategy is one that has been used to great extent in modern hedge-funds, for its simplicity and inherent market-neutral qualities. This strategy, often termed a statistical-arbitrage, relies on monitoring the correlation between a pair of stocks (known to be correlated). A long position is opened on the stock that rises and a short position is opened on the stock that falls. The underlying assumption in pairs-trading is that pairs of stocks, that have historically shown similarities in their behavior will eventually converge in the long run, even if they diverge in the short term, allowing the trader to profit off the pair regardless of the market. 

In such a strategy, identification of correlated stocks and generation of pairs is of paramount importance. In this project, we employ unsupervised learning techniques that include Desnity Based Spatial Cluster of Applications with Noise and K-Means Algorithm. Once, the relevant pairs have been identified, their price relations are extrapolated using supervised learning techniques such as Linear Regression. This overall methodoldogy will help provide insight into the relations between various stocks and facilate the generation of appropriate trading strategies for them.  

## Dataset and Principal Component Analysis

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

## Clustering Analysis

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
