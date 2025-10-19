"""
The classical "Pigeon-hole" problem.
It can be useful to test the efficiency of filtering/reasoning algorithms.

## Data
  An integer n

## Model
  There are two variants: a main one, and a variant "dec"

  constraints: AllDifferent

## Execution:
  python Pigeons.py -data=number
  python Pigeons.py -data=number -variant=dec

## Links
  - https://en.wikipedia.org/wiki/Pigeonhole_principle

## Tags
  academic
"""

from pycsp3 import *

assert not variant() or variant("dec")

n = data or 8  # number of pigeons

# p[i] is the hole where is put the ith pigeon
p = VarArray(size=n, dom=range(n - 1))

if not variant():
    satisfy(
        AllDifferent(p)
    )

elif variant("dec"):
    satisfy(
        p[i] != p[j] for i, j in combinations(n, 2)
    )
