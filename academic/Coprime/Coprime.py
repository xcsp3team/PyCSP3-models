"""
From Akgun et al.'s JAIR'25 paper:
    Erdős and Sárközy studied a range of problems involving coprime sets.
    A pair of numbers a and b are coprime if there is no integer n > 1 which is a factor of both a and b.
    The Coprime Sets problem of size k is to find the smallest m such that there is a subset of k distinct numbers from {m/2 . . . m} that are pairwise coprime.

The model, below, is close to (can be seen as the close translation of) the one proposed in [Akgun et al. JAIR, 2025].
See Experimental Data for TabID Journal Paper (URL given below).

## Data
  a number n

## Execution
  python Coprime.py -data=number
  python Coprime.py -data=number -variant=table

## Links
  - https://www.jair.org/index.php/jair/article/view/17032/27165
  - https://pure.york.ac.uk/portal/en/datasets/experimental-data-for-tabid-journal-paper
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  academic, xcsp25
"""

from pycsp3 import *

n = data or 10

D = range(2, n * n + 1)

# x[i] is the value of the ith element of the coprime set
x = VarArray(size=n, dom=D)

satisfy(
    # setting a lower-bound
    [x[i] >= x[-1] // 2 for i in range(n - 1)],

    # tag(symmetry-breaking)
    Increasing(x, strict=True)
)

if variant("table"):
    cache = {}


    def T(d):
        if d not in cache:
            cache[d] = [(u, v) for u in D for v in D if u % d != 0 or v % d != 0]
        return cache[d]


    satisfy(
        # ensuring that we have coprime integers
        (x[i], x[j]) in T(d) for i, j in combinations(n, 2) for d in D
    )

else:
    satisfy(
        # ensuring that we have coprime integers
        either(
            x[i] % d != 0,
            x[j] % d != 0
        ) for i, j in combinations(n, 2) for d in D

    )

minimize(
    # minimizing the highest value of the set
    x[-1]
)

"""
1) The variant 'table' is used for the track MiniCSP in 2025
2) Data used for the 2025 competition are: [8, 10, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 40]
"""
