"""
Problem 133 on CSPLib.

The knapsack problem or rucksack problem is a problem in combinatorial optimization.

## Data Example
  20-50-00.json

## Model
  constraints: Sum

## Execution
  python Knapsack.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob133/
 - https://en.wikipedia.org/wiki/Knapsack_problem

## Tags
  recreational, csplib
"""

from pycsp3 import *

capacity, items = data or load_json_data("20-50-00.json")

weights, values = zip(*items)
nItems = len(items)

# x[i] is 1 iff the ith item is selected
x = VarArray(size=nItems, dom={0, 1})

satisfy(
    # not exceeding the capacity of the knapsack
    x * weights <= capacity
)

maximize(
    # maximizing summed up value (benefit)
    x * values
)
