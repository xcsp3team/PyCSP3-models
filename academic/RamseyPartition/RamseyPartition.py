"""
See http://www.mathematik.uni-bielefeld.de/~sillke/PUZZLES/partion3-ramsey

Partition the integers 1 to n into three sets, such that for no set are
there three different numbers with two adding to the third.
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

## Data Example
   two integers q and n

## Model
  constraints: Cardinality, NValues

## Execution
  python RamseyPartition.py -data=[number,number]
  python RamseyPartition.py -data=[number,number] -variant=equ


## Links
  - http://www.mathematik.uni-bielefeld.de/~sillke/PUZZLES/partion3-ramsey
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, xcsp25
"""

from pycsp3 import *

assert not variant() or variant("equ") or variant("mini")

q, n, = data or (3, 23)

L = n // q if variant("equ") or variant("mini") else range(3, n)
Q = range(q)

# x[i] is the set (index) where is put the value (i+1)
x = VarArray(size=n, dom=range(q))

if variant("mini"):
    Ts = [[(w, 1 if v == w else 0) for w in Q] for v in Q]

    T = [(u, v, w) for u in Q for v in Q for w in Q if not (u == v == w)]

    y = VarArray(size=[n, q], dom={0, 1})

    satisfy(
        [(x[i], y[i][v]) in Ts[v] for i in range(n) for v in Q],

        [Sum(y[:, v]) == L for v in Q],

        [(x[i], x[j], x[k]) in T for i, j, k in combinations(n, 3) if i + 1 + j + 1 == k + 1]
    )

else:

    satisfy(
        # ensuring some occurrences are guaranteed
        Cardinality(x, occurrences={v: L for v in Q}),

        # ensuring no three different numbers with two adding to the third in teh same set
        [NValues(x[i], x[j], x[k]) > 1 for i, j, k in combinations(n, 3) if i + 1 + j + 1 == k + 1]
    )

""" Comments
1) Data used for the 2025 competition are: [(3, 300), (3, 600), (3, 1200), (4, 60), (4, 62), (4, 64), (4, 80), (4, 100), (4, 400), (5, 130), (5, 140),
   (5, 160), (5, 180), (5, 200),  (5, 400)]
"""
