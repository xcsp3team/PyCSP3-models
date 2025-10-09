"""
The Multi dimensional knapsack problem, as originally proposed as an optimization problem by the OR community.
Note that a feasibility version (where the objective has been fixed) is used in (Refalo, CP 2004) and (Pesant et al., JAIR 2012).

## Data Example
  OR05x100-25-1.json

## Model
  constraints: Sum

## Execution
  python MultiKnapsack.py -data=<datafile.json>
  python MultiKnapsack.py -data=<datafile.txt> -parser=MultiKnapsack_Parser.py

## Links
  - https://www.researchgate.net/publication/271198281_Benchmark_instances_for_the_Multidimensional_Knapsack_Problem
  - https://link.springer.com/chapter/10.1007/978-3-540-30201-8_41
  - https://jair.org/index.php/jair/article/view/10748

## Tags
 recreational
"""

from pycsp3 import *

weights, constraints = data or load_json_data("OR05x100-25-1.json")

n = len(weights)

# x[i] is 1 iff the ith item is selected
x = VarArray(size=n, dom={0, 1})

satisfy(
    x * coefficients <= k for (coefficients, k) in constraints
)

maximize(
    x * weights
)
