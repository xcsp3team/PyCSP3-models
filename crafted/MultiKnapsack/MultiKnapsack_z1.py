"""
Multi Dimensional Knapsack Problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01-06.json

## Model
  constraints: Sum

## Execution
  python MultiKnapsack_z1.py -data=<datafile.json>
  python MultiKnapsack_z1.py -data=<datafile.dzn> -parser=MultiKnapsack_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  crafted, mzn14
"""

from pycsp3 import *

weights, profits, sizes, z = data or load_json_data("01-06.json")

nItems, nBins = len(profits), len(sizes)

# x[i] is 1 if the ith item is selected
x = VarArray(size=nItems, dom={0, 1})

satisfy(
    # not exceeding the capacity of each bin
    [x * weights[j] <= sizes[j] for j in range(nBins)],

    # ensuring we get the fixed objective value
    profits * x == z
)
