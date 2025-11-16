"""
Deriving the optimal wiring sequence for a given layout of a cable tree.
See paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  A031.json

## Model
  constraints: Maximum, Sum

## Execution
  python CableTreeWiring.py -data=<datafile.json>
  python CableTreeWiring.py -data=<datafile.dzn> -parser=CableTreeWiring_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-021-09321-w
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn20, mzn24
"""

from pycsp3 import *

nCavities, nWiredCavityPairs, atomic, disjunctive, soft, direct = data or load_json_data("A031.json")

b = nWiredCavityPairs
assert b > 0 and isinstance(direct, list), str(direct)

# x[i] is the position of the ith cavity
x = VarArray(size=nCavities, dom=range(nCavities))

satisfy(
    AllDifferent(x),

    [x[i] < x[j] for i, j in atomic],

    [
        either(
            x[i] < x[j],
            x[k] < x[q]
        ) for i, j, k, q in disjunctive
    ],

    [
        If(
            x[j] < x[j + b],
            Then=x[j] + 1 == x[j + b]
        ) for j in direct if j < b
    ],

    [
        If(
            x[j] < x[j - b],
            Then=x[j] + 1 == x[j - b]
        ) for j in direct if j >= b
    ],

    [
        either(
            x[i] < x[j],
            x[i] < x[q]
        ) for i, j, k, q in disjunctive if i == k
    ]
)

tmp = [
    [
        both(
            x[j] < x[i],
            x[i] < x[j + g]
        ) for j in range(2 * b) for g in [b if j < b else -b] if i not in {j, j + g}
    ] for i in range(2 * b)
]

minimize(
    Sum(abs(x[i] - x[i + b]) > 1 for i in range(b)) * nCavities ** 3
    +
    Maximum(Sum(t) for t in tmp) * nCavities ** 2
    +
    Maximum(abs(x[i] - x[i + b]) - 1 for i in range(b)) * nCavities
    +
    Sum(x[i] > x[j] for i, j in soft)
)

""" Comments
1) Note that:
 either(x[i] < x[j], x[k] < x[l])
  is equivalent to:
   (x[i] < x[j]) | (x[k] < x[l])
2) Note that:
  both(x[j] < x[i], x[i] < x[j + g])
   is equivalent to:
  (x[j] < x[i]) & (x[i] < x[j + g])
3) A useless array is present in the minizinc model.
 if variant("mz"):
     y = VarArray(size=k, dom=range(k))

     satisfy(
         AllDifferent(y)
     )
"""
