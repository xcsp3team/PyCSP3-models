"""
In this variation of the knapsack problem, the weight of knapsack item i is given by a D-dimensional vector
wi = (wi1 , . . . , wiD ) and the knapsack has a D-dimensional capacity vector (W1 , . . . , WD ).
The target is to maximize the sum of the values of the items in the knapsack so that
the sum of weights in each dimension d does not exceed Wd .
See Wikipedia.

## Data (example)
  OR05x100-25-1.json

## Model
  constraints: Knapsack, Sum

## Execution
  - python GeneralizedMKP.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Knapsack_problem
  - https://www.researchgate.net/publication/271198281_Benchmark_instances_for_the_Multidimensional_Knapsack_Problem
  - https://www.minizinc.org/challenge2019/results2019.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, mzn15, mzn19, xcsp23
"""

from pycsp3 import *

profits, wmatrix, capacities, pmatrix = data  # , pmatrix = data
nItems, nBins = len(profits), len(capacities)

# x[i] is 1 if the item i is packed
x = VarArray(size=nItems, dom={0, 1})

# w[j] si the total weight in the jth bin
w = VarArray(size=nBins, dom=lambda j: range(capacities[j] + 1))

z = Var(range(sum(profits) + 1))

satisfy(
    [Knapsack(x, weights=weights, wlimit=w[j], profits=pmatrix[j]) >= z for j, weights in enumerate(wmatrix)],

    # computing the objective value
    z == profits * x
)

maximize(
    # maximizing the profit of packed items
    z
)

""" Comments
1) Wrt the minizinc model, must we write  >= opt or == opt ?

2) one can write wcondition=eq(w[j]) or wcondition=le(w[j]) or wlimit=w[j]

3) for being compatible with the competition mini-track, we use:
  [x * weights <= w[j] for j, weights in enumerate(wmatrix)],
  [x * pmatrix[j] >= z for j, weights in enumerate(wmatrix)],
"""
