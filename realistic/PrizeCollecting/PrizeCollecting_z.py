"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2016 Minizinc challenges.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  25-5-5-9.json

## Model
  constraints: Count, Element, Sum

## Execution
  python PrizeCollecting_z.py -data=<datafile.json>
  python PrizeCollecting_z.py -data=<datafile.dzn> -parser=PrizeCollecting_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2016/results/

## Tags
  realistic, mzn11, mzn16
"""

from pycsp3 import *

n, prizes = data

N = range(n)

# p[i] is the position (starting at 0) of the ith node in the tour (-1 if unused)
p = VarArray(size=n, dom=range(-1, n))

# succ[i] is the node that succeeds to the ith node in the tour (value i if unused)
succ = VarArray(size=n, dom=range(n))

# gold[i] is the gold (gain) collected when going from the ith node to its successor in the tour
gold = VarArray(size=n, dom=lambda i: prizes[i])

satisfy(
    # node 0 is the first node of the tour
    p[0] == 0,

    # managing unused nodes
    [(p[i] != -1) == (succ[i] != i) for i in N],

    # each node appears at most once during the tour
    [AtMostOne(within=succ, value=i) for i in N],

    # if used and not last (0), we link positions
    [
        If(
            succ[i] != i, succ[i] != 0,
            Then=p[succ[i]] == p[i] + 1
        ) for i in N
    ],

    # computing gains
    [gold[i] == prizes[i][succ[i]] for i in N]
)

maximize(
    # maximizing the sum of collected gains
    Sum(gold)
)
