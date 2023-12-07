"""
See paper cited below.

## Data
  An integer n

## Model
  constraints: Element

## Execution:
  python LangfordBin.py -data=number

## Links
  - https://link.springer.com/chapter/10.1007/11889205_15

## Tags
  academic
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
