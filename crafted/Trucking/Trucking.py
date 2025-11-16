"""
There are some trucks.
Each truck can transport a given Load of material, and has an associated cost.
In each time period a demand has to be fulfilled.
The trucks number 1 and 2 have some further constraints, disallowing them to be used more than once
in consecutive or two consecutive time periods.
The goal is to minimise the overall cost.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
The original MZN model was proposed by Jakob Puchinger - no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01.json

## Model
  constraints: Count, Sum

## Execution
  python Trucking.py -data=<datafile.json>
  python Trucking.py -data=<datafile.dzn> -parser=Trucking_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  crafted, mzn08
"""

from pycsp3 import *

costs, loads, demands, truck1, truck2 = data or load_json_data("01.json")

nTrucks, horizon = len(costs), len(demands)

# x[i][t] is 1 if the ith truck is used at time t
x = VarArray(size=[nTrucks, horizon], dom={0, 1})

satisfy(
    # the demand must be satisfied at any time
    [loads * x[:, t] >= demands[t] for t in range(horizon)],

    # truck1 cannot be used more than once in three consecutive time periods
    [AtMostOne(x[truck1][t:t + 3]) for t in range(horizon - 2)],

    # truck2 cannot be used more than once in two consecutive time periods
    [AtMostOne(x[truck2][t: t + 2]) for t in range(horizon - 1)]
)

minimize(
    # minimizing the overall cost
    Sum(costs[i] * Sum(x[i]) for i in range(nTrucks))
)

""" Comments
1) [AtMostOne(x[truck2][t: t + 2]) for t in range(horizon - 1)]
 is mmediate (to understand at first sight) than:
   [Sum(x[truck2][t: t + 2]) <= 1 for t in range(horizon - 1)]
 which, itself, is more compact than: 
   [Sum(x[truck2][t] for t in range(t, t + 2)) <= 1 for t in range(horizon - 1)]
"""
