# Problem Auction
## Description
[Problem 063](https://www.csplib.org/Problems/prob063/) on CSPLib :

There is a bunch of people bidding for things. A bid has a value, and the bid is for a set of items. If we have two bids, call them A and B, and there is an intersection on the items they bid for, then we can accept bid A or bid B, but we cannot accept both of them. However, if A and B are bids on disjoint sets of items then these two bids are compatible with each other, and we might accept both. The problem then is to accept compatible bids such that we maximise the sum of the values of those bids (i.e. make most money).

## Data
A set of bids. Each bid has a value and has a set of items.
An example is provided in the json file.

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)


## Command Line
```
  python Auction.py [-solve]
  python Auction.py -data=Auction_example.json
```

## Tags
 recreational csplib
