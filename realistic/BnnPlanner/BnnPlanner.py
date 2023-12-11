"""
Planning with Learned Binarized Neural Networks.
See AIJ paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Buser Say.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  sysadmin-4-2S.json

## Model
  constraints: Sum

## Execution
  python BnnPlanner.py -data=<datafile.json>
  python BnnPlanner.py -data=<datafile.dzn> -parser=BnnPlanner_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0004370220300503
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

n, eq_constraints, ge_constraints, iff_constraints, (AA, BB) = data

# x[i] is the value (0 or 1) of the ith variable
x = VarArray(size=n, dom={0, 1})

satisfy(
    # respecting eq constraints
    [A * x[B] == k for A, B, k in eq_constraints],

    # respecting ge constraints
    [A * x[B] >= k for A, B, k in ge_constraints],

    # respecting iff constraints
    [x[i] == (A * x[B] >= k) for i, A, B, k in iff_constraints]
)

minimize(
    AA * x[BB]
)

"""
1) having coefficients (A) and indexes (B) separate avoids slowing down posting constraints, as in:
 [Sum(c[i * 2] * x[c[i * 2 + 1] - 1] for i in range(len(c) // 2)) == c[-1] for c in ceq],
 [Sum(c[i * 2] * x[c[i * 2 + 1] - 1] for i in range(len(c) // 2)) >= c[-1] for c in cge],
 [x[c[0] - 1] == (Sum(c[i * 2 + 1] * x[c[i * 2 + 2] - 1] for i in range(len(c) // 2 - 1)) >= c[-1]) for c in ciff]
"""
