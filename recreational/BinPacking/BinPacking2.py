"""
A Bin Packing Problem.

The bin packing problem (BPP) can be informally defined in a very simple way.
We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c.
The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.

## Data Example
  n1c1w4a.json

## Model
  constraints: BinPacking, NValues

## Execution
  python BinPacking2.py -data=<datafile.json>

## Links
  - https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
"""

from pycsp3 import *
from math import ceil

capacity, weights = data  # bin capacity and item weights
weights.sort()
nItems = len(weights)


def n_bins():
    cnt = 0
    curr_load = 0
    for weight in weights:
        curr_load += weight
        if curr_load > capacity:
            cnt += 1
            curr_load = weight
    return cnt


def series():
    t = []
    start = 0
    for i, weight in enumerate(weights):
        if weight == weights[start]:
            continue
        if start < i - 1:
            t.append((start, i - start))
        start = i
    return t


def w(a, b, *, bar=False):
    if bar:
        return [i for i, weight in enumerate(weights) if a <= weight <= b]
    return [i for i, weight in enumerate(weights) if a < weight <= b]


def lb2(v=None):
    half = len(w(capacity // 2, capacity))
    if v is None:
        return max(lb2(vv) for vv in range(capacity // 2 + 1))
    return half + max(0, ceil(sum(weights[i] for i in w(v, capacity - v, bar=True)) / capacity - len(w(capacity // 2, capacity - v))))


nBins = n_bins()
n_exceeding = len([weight for weight in weights if weight > capacity // 2])

# x[i] is the bin (number) where is put the ith item
x = VarArray(size=nItems, dom=range(nBins))

# z is the number of used bins
z = Var(range(lb2(), nBins + 1))

satisfy(
    # ensuring that the capacity of each bin is not exceeded
    BinPacking(x, sizes=weights) <= capacity,

    # ensuring a minimum number of bins
    z == NValues(x),  # >= ceil(sum(weights) / capacity),

    # tag(symmetry-breaking)
    [Increasing(x[s:s + l]) for (s, l) in series()],

    # tag(symmetry-breaking)
    [x[nItems - n_exceeding + i] == i for i in range(n_exceeding)]
)

minimize(
    # minimizing the number of used bins
    z  # NValues(x)
)

"""
1) better lower bound scan (lb3), to be computed. here, we use lb2:
    print("lb1", ceil(sum(weights) / capacity))
    print("lb2", lb2())
"""
