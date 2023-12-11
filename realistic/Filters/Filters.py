"""
This problem is about optimizing the scheduling of filter operations, commonly used in High-Level Synthesis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Krzysztof Kuchcinski.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  ar1-3.json

## Model
  constraints: NoOverlap, Maximum

## Execution
  python Filters.py -data=<datafile.json>
  python Filters.py -data=<datafile.dzn> -parser=Filters_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S1383762103000754
  - https://github.com/radsz/jacop/tree/develop/src/main/java/org/jacop/examples/fd/filters
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn10, mzn12, mzn13, mzn16
"""

from pycsp3 import *

del_add, del_mul, number_add, number_mul, last, add, dependencies = data
nOperations = len(dependencies)

d = [del_add if i in add else del_mul for i in range(nOperations)]  # durations
mul = [i for i in range(nOperations) if i not in add]

# x[i] is the starting time of the ith operation
x = VarArray(size=nOperations, dom=range(101))

# y[i] is the (index of the) operator used for the ith operation
y = VarArray(size=nOperations, dom=lambda i: range(1, 1 + (number_add if i in add else number_mul)))

satisfy(
    # respecting dependencies
    [x[i] + d[i] <= x[j] for i in range(nOperations) for j in dependencies[i]],

    # no overlap concerning add operations
    NoOverlap(origins=[(x[i], y[i]) for i in add], lengths=[(del_add, 1) for i in add]),

    # no overlap concerning mul operations
    NoOverlap(origins=[(x[i], y[i]) for i in mul], lengths=[(del_mul, 1) for i in mul])
)

minimize(
    # minimizing the ending time of last operations
    Maximum(x[i] + d[i] for i in last)
)
