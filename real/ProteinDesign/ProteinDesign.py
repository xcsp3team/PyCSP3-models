"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2018 Minizinc challenges.
The MZN model was proposed by Simon de Givry.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  test.json

## Model
  constraints: Sum, Table

## Execution
  python ProteinDesign.py -data=<datafile.json>
  python ProteinDesign.py -data=<datafile.dzn> -parser=ProteinDesign_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn13, mzn18
"""

from pycsp3 import *

n, d, maxCosts1, maxCosts2, c1s, c2s = data
e1, e2 = len(c1s), len(c2s)

# x[i] is the value for the ith variable
x = VarArray(size=n, dom=range(0, d))

# c1|i] is the cost of the ith unary soft constraint
c1 = VarArray(size=e1, dom=range(maxCosts1 + 1))

# c2|i] is the cost of the ith binary soft constraint
c2 = VarArray(size=e2, dom=range(maxCosts2 + 1))

satisfy(
    # unary cost functions
    [(c1[k], x[i]) in [t[i * 2:i * 2 + 2] for i in range(len(t) // 2)] for k, (i, t) in enumerate(c1s)],

    # binary cost functions
    [(c2[k], x[i], x[j]) in [t[i * 3:i * 3 + 3] for i in range(len(t) // 3)] for k, (i, j, t) in enumerate(c2s)]
)

minimize(
    # minimizing the sum of costs
    Sum(c1) + Sum(c2)
)
