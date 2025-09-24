"""
From paper (by Gent, Jefferson and Miguel at CP'06]:
    Langford’s Problem L(k, n) requires ﬁnding a list of length k∗n, which contains k sets of the numbers 1 to n,
    such that for all m ∈ {1, 2, ..., n} there is a gap of size m between adjacent occurrences of m.
    In the constraint solver Minion, L(2,n) was modelled using two vectors of variables, V and P, each of size 2n.
    Each variable in V has domain {1, 2, ..., n}, and V represents the result.
    For each i ∈ {1, 2, ...} the 2ith and 2i + 1st variables in P are the ﬁrst and second positions of i in V.
    Each variable in P has domain {0, 1, ..., 2n−1}, indexing matrices from 0.

## Data
  An integer n

## Model
  constraints: Element

## Execution:
  python LangfordBin.py -data=number

## Links
  - https://link.springer.com/chapter/10.1007/11889205_15
  - https://www.csplib.org/Problems/prob024/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, csplib, xcsp25
"""

from pycsp3 import *

n = data or 8

# v[i] is the ith value of the Langford's sequence
v = VarArray(size=2 * n, dom=range(1, n + 1))

# p[j] is the first (resp., second) position of 1+j/2 in v if j is even (resp., odd)
p = VarArray(size=2 * n, dom=range(2 * n))

satisfy(
    [v[p[2 * i]] == i + 1 for i in range(n)],

    [v[p[2 * i + 1]] == i + 1 for i in range(n)],

    [p[2 * i] == i + 2 + p[2 * i + 1] for i in range(n)]
)

"""
1) Data used for the 2025 competition are: [10, 13, 14, 16, 39, 40, 59, 60, 79, 80, 120, 240]
"""
