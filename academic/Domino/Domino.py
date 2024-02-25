"""
This problem is described in the paper cited below.
Informally the Domino problem is an undirected constraint graph with a cycle and a trigger constraint.

## Data
  a pair (n,d), where n is the number of variables and d the size of the domain

## Model
  There are two variants: a main one and a variant 'table' with constraints in extension.

  constraints: AllEqual, Table

## Execution
  python Domino.py
  python Domino.py -data=[number,number]
  python Domino.py -data=[number,number] -variant=table

## Links
  - https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.103.1730&rep=rep1&type=pdf

## Tags
  academic
"""

from pycsp3 import *

n, d = data  # number of dominoes and number of values

# x[i] is the value of the ith domino
x = VarArray(size=n, dom=range(d))

if not variant():
    satisfy(
        AllEqual(x),

        either(
            x[0] + 1 == x[-1],
            Or=both(x[0] == x[-1], x[0] == d - 1)
        )
    )

elif variant("table"):
    satisfy(
        [(x[i], x[i + 1]) in {(v, v) for v in range(d)} for i in range(n - 1)],

        (x[0], x[-1]) in {(v + 1, v) for v in range(d - 1)} | {(d - 1, d - 1)}
    )

""" Comments
1) Note that it is not possible to write: x[0] == x[-1] == v - 1
"""
