"""
Problem 063 on CSPLib.

There is a bunch of people bidding for things. A bid has a value, and the bid is for a set of items. If we have two bids, call them A and B, and there is an intersection on the items they bid for, then we can accept bid A or bid B, but we cannot accept both of them. However, if A and B are bids on disjoint sets of items then these two bids are compatible with each other, and we might accept both. The problem then is to accept compatible bids such that we maximise the sum of the values of those bids (i.e. make most money).

## Data
  example.json

## Model
  constraints: Count, Sum

## Command Line
  python Auction.py [-solve]
  python Auction.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob063/

## Tags
  realistic, csplib
"""

from pycsp3 import *

bids = data or default_data("example.json")
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

"""
1) we avoid using values instead of vals as name for the list of bid values 
   as it may enter in conflict with the function values() in a notebook 
"""
