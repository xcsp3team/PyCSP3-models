"""
This is a particular case of the Discrete Lot Sizing Problem (DLSP); see Problem 058 on CSPLib.

## Data (example)
  001.json

## Model
  constraints: Sum

## Execution
  - python PSP1.py -data=<datafile.json>
  - python PSP1.py -data=<datafile.txt> -parser=PSP_Parser.py

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://github.com/xgillard/mznlauncher
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, csplib, xcsp23
"""

from pycsp3 import *

nOrders, changeCosts, stockingCosts, demands = data
nItems, horizon = len(demands), len(demands[0])

# x[t][i] is 1 when item i is produced at time t
x = VarArray(size=[horizon, nItems], dom={0, 1})

# y[t][i] is 1 if the machine is ready to produce i at time t
y = VarArray(size=[horizon, nItems], dom={0, 1})

# c[t][i] is 1 if the configuration changes from i to j at time t
c = VarArray(size=[horizon, nItems, nItems], dom=lambda t, i, j: {0, 1} if t != 0 and i != j else None)

# s[t][i] is the number of items of type i stored at time t
s = VarArray(size=[horizon + 1, nItems], dom=lambda t, i: range(sum(demands[i]) + 1))

satisfy(
    # the stock of every item is empty at startup
    s[0] == 0,

    # when an item is produced, it is either delivered or stocked for later delivery
    [x[t][i] + s[t][i] == demands[i][t] + s[t + 1][i] for t in range(horizon) for i in range(nItems)],

    # consistency between production and machine setup
    [x[t][i] <= y[t][i] for t in range(horizon) for i in range(nItems)],

    # only 1 unit of one item is produced at each time
    [Sum(y[t]) == 1 for t in range(horizon)],

    # consistency between machine setup and changeover
    [c[t][i][j] >= y[t - 1][i] + y[t][j] - 1 for t in range(1, horizon) for i in range(nItems) for j in range(nItems) if i != j]
)

minimize(
    Sum(changeCosts[i][j] * Sum(c[:, i, j]) for i in range(nItems) for j in range(nItems) if i != j)
    + Sum(stockingCosts[i] * Sum(s[:, i]) for i in range(nItems))
)

""" Comments
1) it seems to be more efficient to write:
  [(c[t][i][j], y[t - 1][i], y[t][j]) not in {(0, 1, 1)} for t in range(1, horizon) for i in range(nItems) for j in range(nItems) if i != j]
than
  c[t][i][j] >= y[t - 1][i] + y[t][j] - 1 for t in range(1, horizon) for i in range(nItems) for j in range(nItems) if i != j]
2) for being compatible with the competition mini-track, we use:
  sp = VarArray(size=[horizon + 1, nItems], dom=lambda t, i: range(sum(demands[i]) + 2))
  
  [sp[t][i] == x[t][i] + s[t][i] for t in range(horizon) for i in range(nItems)],

  # when an item is produced, it is either delivered or stocked for later delivery
  [sp[t][i] == demands[i][t] + s[t + 1][i] for t in range(horizon) for i in range(nItems)],
"""
