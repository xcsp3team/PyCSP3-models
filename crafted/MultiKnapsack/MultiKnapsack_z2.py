"""
Multi Dimensional Knapsack Problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01-06.json

## Model
  constraints: Knapsack, Sum

## Execution
  python MultiKnapsack_z2.py -data=<datafile.json>
  python MultiKnapsack_z2.py -data=<datafile.dzn> -parser=MultiKnapsack_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  crafted, mzn15, mzn19
"""

from pycsp3 import *

weightsPerBin, profits, binSizes, z = data
nItems, nBins = len(profits), len(binSizes)

# x[i] is 1 if the item i is packed
x = VarArray(size=nItems, dom={0, 1})

# w[j] si the total weight in the jth bin
w = VarArray(size=nBins, dom=lambda j: range(binSizes[j] + 1))

satisfy(
    Knapsack(x, weights=weights, wlimit=w[j], profits=profits) == z for j, weights in enumerate(weightsPerBin)
)

maximize(
    # maximizing the profit of packed items
    profits * x
)

"""
1) Wrt the minizinc model, must we write  >= z or == z ?

2) one can write wcondition=eq(w[j]) or wcondition=le(w[j]) or wlimit=w[j]
"""
