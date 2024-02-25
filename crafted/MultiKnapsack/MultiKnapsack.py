"""
The Multi dimensional knapsack problem was originally proposed as an optimization problem by the OR community.
Here, it is the feasibility version, as used, e.g., in (Refalo, CP 2004) and (Pesant et al., JAIR 2012).

## Data Example
  OR05x100-25-1.json

## Model
  constraints: Sum

## Execution
  python MultiKnapsack.py -data=<datafile.json>
  python MultiKnapsack.py -data=<datafile.txt> -parser=MultiKnapsack_Parser.py

## Links
  - https://www.researchgate.net/publication/271198281_Benchmark_instances_for_the_Multidimensional_Knapsack_Problem

## Tags
 recreational
"""

from pycsp3 import *

weights, constraints = data
n = len(weights)

# x[i] is 1 iff the ith item is selected
x = VarArray(size=n, dom={0, 1})

satisfy(
    x * C <= k for (C, k) in constraints
)

maximize(
    x * weights
)
