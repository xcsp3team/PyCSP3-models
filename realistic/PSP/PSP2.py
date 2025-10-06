"""
This is a particular case of the Discrete Lot Sizing Problem (DLSP); see Problem 058 on CSPLib.

## Data Example
  001.json

## Model
  constraints: Count, Element, Sum

## Execution
  python PSP2.py -data=<datafile.json>
  python PSP2.py -data=<datafile.txt> -parser=PSP_Parser.py

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://github.com/xgillard/mznlauncher
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, csplib, xcsp23
"""

from pycsp3 import *

nOrders, changeCosts, stockingCosts, demands = data or load_json_data("001.json")

nItems, horizon = len(demands), len(demands[0])

required = [[sum(demands[i][:t + 1]) for t in range(horizon)] for i in range(nItems)]

# x[t] is the item produced at time t
x = VarArray(size=horizon, dom=range(nItems))

# p[i][t] is 1 if the ith item is produced at time t
p = VarArray(size=[nItems, horizon], dom={0, 1})

# z[t] is the changeover cost incurred at time t
z = VarArray(size=horizon - 1, dom=changeCosts)

satisfy(
    # channeling variables
    [
        p[i][t] == (x[t] == i)
        for i in range(nItems) for t in range(horizon)
    ],

    # ensuring that deadlines of demands are respected
    [
        Sum(p[i][:t + 1]) >= required[i][t]
        for i in range(nItems) for t in range(horizon) if t == 0 or required[i][t - 1] != required[i][t]
    ],

    # computing changeover costs
    [
        z[t] == changeCosts[x[t], x[t + 1]]
        for t in range(horizon - 1)
    ],

    # tag(redundant)
    [
        Count(within=x, value=i) >= required[i][-1]
        for i in range(nItems)
    ]
)

minimize(
    Sum(stockingCosts[i] * (Sum(p[i][:t + 1]) - required[i][t]) for i in range(nItems) for t in range(horizon))
    + Sum(z)
)

""" Comments
1) We post a subset of constraints about deadlines only when a skip
2) Should we compute Sum(p[i][:t + 1]) - required[i][t] with variables?
3) -rr -ale=5 : interesting to convert into extension (how to decide this?)
"""

# [ift(x[t] != x[t + 1], z[t] == changeCosts[x[t], x[t + 1]], z[t] == 0) for t in range(horizon - 1)],
