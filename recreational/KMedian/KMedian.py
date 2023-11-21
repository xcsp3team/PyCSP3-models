"""
The k-median problem (with respect to the 1-norm) is the problem of finding k centers such that the clusters formed by them are the most compact.
Formally, given a set of data points, the k centers ci are to be chosen so as to minimize the
sum of the distances from each data point to the nearest ci.

## Data (example)
  pmed01.json

## Model
  constraints: AllDifferent, Minimum, Sum

## Execution
  - python KMedian.py -data=<datafile.json>
  - python KMedian.py -data=<datafile.json> -variant=aux
  - python KMedian.py -data=<datafile.txt> -parser=KMedian_Parser.py

## Links
  -https://en.wikipedia.org/wiki/K-medians_clustering
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  recreational, xcsp23
"""

from pycsp3 import *

distances, k = data
n = len(distances)

# x[i] is the ith selected node
x = VarArray(size=k, dom=range(n))

satisfy(
    # selected nodes must be all different
    AllDifferent(x),

    # tag(symmetry-breaking)
    Increasing(x, strict=True)
)

if not variant():
    minimize(
        # minimizing the minimal distances between nodes and the selected ones
        Sum(Minimum(distances[c][j] for c in x) for j in range(n))
    )

elif variant("aux"):

    # d[i][j] is the distance between the ith selected node and the jth node
    d = VarArray(size=[k, n], dom=distances)

    satisfy(
        # computing distances
        d[i][j] == distances[:, j][x[i]] for i in range(k) for j in range(n)
    )

    minimize(
        # minimizing the minimal distances between nodes and the selected ones
        Sum(Minimum(d[:, j]) for j in range(n))
    )

""" Comments
1) generating the first variant may be very time expensive

2) the two-dimensional array called distances used as domain is automatically transformed into a set of integers
"""
