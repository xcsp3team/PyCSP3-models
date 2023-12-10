"""
Given a set of subsets S_1,...,S_m$of the universal set U={1,...,n},
find the smallest subset of subsets T of S such that their union is U.

## Data Example
  example.json

## Model
  constraints: Count, Sum

## Execution
  python SetCovering.py -data=<datafile.json>

## Links
  - https://algorist.com/problems/Set_Cover.html

## Tags
  recreational
"""

from pycsp3 import *

subsets = data
values = sorted({v for subset in subsets for v in subset})
m = len(subsets)

# x[i] is 1 iff the ith subset is selected
x = VarArray(size=m, dom={0, 1})

satisfy(
    # ensuring the presence of each value
    Count(scp, value=1) >= 1 for scp in [[x[i] for i, subset in enumerate(subsets) if v in subset] for v in values]
)

minimize(
    # minimizing the number of selected subsets
    Sum(x)
)
