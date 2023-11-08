"""
Problem 063 on CSPLib.<br />

There is a bunch of people bidding for things. A bid has a value, and the bid is for a set of items. If we have two bids, call them A and B, and there is an intersection on the items they bid for, then we can accept bid A or bid B, but we cannot accept both of them. However, if A and B are bids on disjoint sets of items then these two bids are compatible with each other, and we might accept both. The problem then is to accept compatible bids such that we maximise the sum of the values of those bids (i.e. make most money).

## Data
A set of bids. Each bid has a value and has a set of items.
An example is provided in the json file.

## Model
constraints: Count, Sum

## Command Line
  python Auction.py [-solve]
  python Auction.py -data=Auction_example.json

## Links
 - https://www.csplib.org/Problems/prob063/

## Tags
 recreational csplib
"""

from pycsp3 import *

bids = data or default_data("data/Auction_example.json")
items = sorted({item for bid in bids for item in bid.items})
values = integer_scaling(bid.value for bid in bids)
nBids = len(bids)

# x[i] is 1 iff the ith bid is selected
x = VarArray(size=nBids, dom={0, 1})

satisfy(
    # avoiding intersection of bids
    Count(scp, value=1) <= 1 for scp in [[x[i] for i, bid in enumerate(bids) if item in bid.items] for item in items]
)

maximize(
    # maximizing summed values of selected bids
    x * values
)
