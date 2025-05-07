"""
A Bin Packing Problem.

The bin packing problem (BPP) can be informally defined in a very simple way.
We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c.
The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.

## Data Example
  n1c1w4a.json

## Model
  There are two variants:
   - one with extension constraints
   - one with sum and decreasing constraints.

  constraints: BinPacking, Cardinality, Lex, Sum, Table

## Execution
  python BinPacking.py -data=<datafile.json>
  python BinPacking.py -data=<datafile.json> -variant=table

## Links
  - https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
"""

from pycsp3 import *
from itertools import groupby
from math import ceil

capacity, weights = data  # bin capacity and item weights
weights.sort()  # in case weights are not sorted
nItems = len(weights)


def n_bins():
    cnt = 0
    curr_load = 0
    for i, weight in enumerate(weights):
        curr_load += weight
        if curr_load > capacity:
            cnt += 1
            curr_load = weight
    return cnt


def max_items_per_bin():
    curr = 0
    for i, weight in enumerate(weights):
        curr += weight
        if curr > capacity:
            return i
    return -1


def w(a, b, *, bar=False):
    if bar:
        return [i for i, weight in enumerate(weights) if a <= weight <= b]
    return [i for i, weight in enumerate(weights) if a < weight <= b]


def lb2(v=None):
    half = len(w(capacity // 2, capacity))
    if v is None:
        return max(lb2(vv) for vv in range(capacity // 2 + 1))
    return half + max(0, ceil(sum(weights[i] for i in w(v, capacity - v, bar=True)) / capacity - len(w(capacity // 2, capacity - v))))


nBins, maxPerBin = n_bins(), max_items_per_bin()

# x[i][j] is the weight of the jth object put in the ith bin. It is 0 if less than j objects are present in the bin.
x = VarArray(size=[nBins, maxPerBin], dom={0, *weights})

# z is the number of used bins
z = Var(range(lb2(), nBins + 1))

if not variant():
    satisfy(
        # not exceeding the capacity of each bin
        [Sum(x[i]) <= capacity for i in range(nBins)],

        # items are stored decreasingly in each bin according to their weights
        [Decreasing(x[i]) for i in range(nBins)]
    )

elif variant("table"):
    def table():
        def table_recursive(n_stored, i, curr):
            assert len(tuples) < 200000000, "impossible to build a table of moderate size"  # hard coding (value)
            assert curr + weights[i] <= capacity
            tmp[n_stored] = weights[i]
            curr += weights[i]
            tuples.append(tuple(tmp[j] if j < n_stored + 1 else 0 for j in range(maxPerBin)))
            for j in range(i):
                if curr + weights[j] > capacity:
                    break
                if j == i - 1 or weights[j] != weights[j + 1]:
                    table_recursive(n_stored + 1, j, curr)

        tmp = [0] * maxPerBin
        tuples = [tuple(tmp)]
        for i in range(nItems):
            if i == nItems - 1 or weights[i] != weights[i + 1]:
                table_recursive(0, i, 0)
        return tuples


    T = table()
    satisfy(
        x[i] in T for i in range(nBins)
    )

satisfy(
    # computing the number of used bins
    z == Sum(x[i][0] != 0 for i in range(nBins)),

    # ensuring that each item is stored in a bin
    Cardinality(
        within=x,
        occurrences={0: nBins * maxPerBin - nItems} | {wgt: len(list(t)) for wgt, t in groupby(weights)}
    ),

    # tag(symmetry-breaking)
    LexDecreasing(x)
)

minimize(
    # minimizing the number of used bins
    z  # Sum(x[i][0] != 0 for i in range(nBins))
)

# maximize(
#     Sum(x[i][0] == 0 for i in range(nBins))
# )
