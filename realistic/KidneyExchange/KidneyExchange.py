"""
Cardinality-constrained Multi-cycle Problem (CCMCP).

This problem appears as one of the main optimization problems modelling kidney exchange.
The problem consists of the prize-collecting assignment problem and an addition constraint stipulating that each subtour in the graph
has a maximum length K.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Edward Lam and Vicky Mak-Hau.
No Licence was explicitly mentioned (MIT Licence is assumed).


## Data Example
  3-20-025-2.json

## Model
  constraints: AllDifferent, BinPacking, Precedence, Sum

## Execution
  python KidneyExchange.py -data=<datafile.json>
  python KidneyExchange.py -data=<datafile.dzn> -parser=KidneyExchange_ParserZ.py
  python KidneyExchange.py -data=<datafile.txt> -parser=KidneyExchange_ParserW.py

## Links
  - https://en.wikipedia.org/wiki/Optimal_kidney_exchange
  - https://www.preflib.org/dataset/00036
  - https://link.springer.com/article/10.1007/s10878-015-9932-4
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, notebook, mzn19, mzn23
"""

from pycsp3 import *

weights, k = data
n = len(weights)

# x[i] is the successor node of node i (in the cycle where i belongs)
x = VarArray(size=n, dom=range(n))

# y[i] is the cycle (index) where the node i belongs
y = VarArray(size=n, dom=range(n))

satisfy(
    AllDifferent(x),

    # ensuring correct cycles
    [y[i] == y[x[i]] for i in range(n)],

    # disabling infeasible arcs
    [x[i] != j for i in range(n) for j in range(n) if i != j and weights[i][j] < 0],

    # each cycle has k as maximum length
    BinPacking(y, sizes=1) <= k,

    # tag(symmetry-breaking)
    Precedence(y)
)

maximize(
    # maximizing the sum of arc weights of selected cycles
    Sum(weights[i][x[i]] for i in range(n))
)
