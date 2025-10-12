"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  02.json

## Model
  constraints: Cumulative, Sum

## Execution
  python Smelt.py -data=<datafile.json>
  python Smelt.py -data=<datafile.dzn> -parser=Smelt_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  realistic, mzn14
"""

from pycsp3 import *

flows, recipes, orders, nLines, rules = data or load_json_data("02.json")

ot, oh, ow = zip(*orders)
rt, rk1, rd, rk2 = zip(*rules)

nMinerals, nRecipes, nOrders, nRules = len(flows), len(recipes), len(orders), len(rules)
durations = [sum(oh[i] * ow[i] for i in range(nOrders) if ot[i] == j) for j in range(nRecipes)]
H = 1000  # horizon

# os[i] is the start time of the ith order
os = VarArray(size=nOrders, dom=range(H + 1))

# ol[i] is the line used for the ith order
ol = VarArray(size=nOrders, dom=range(1, nLines + 1))

# rs[i] is the start time of the ith recipe
rs = VarArray(size=nRecipes, dom=range(H + 1))

# re[i] is the end time of the ith recipe
re = VarArray(size=nRecipes, dom=range(H + 1))

# rl[i] is the line used for the ith recipe
rl = VarArray(size=nRecipes, dom=range(1, nLines + 1))

# f[i] is 1 iff there is no violation of the ith rule
f = VarArray(size=nRules, dom={0, 1})

# m is the make-span wrt recipes
m = Var(dom=range(H + 1))


def production_rule(i):
    assert rt[i] in range(4)
    if rt[i] == 0:
        return re[rk1[i]] + rd[i] <= rs[rk2[i]]
    if rt[i] == 1:
        return re[rk1[i]] + rd[i] >= rs[rk2[i]]
    if rt[i] == 2:
        return rs[rk1[i]] - rd[i] <= rs[rk2[i]]
    return re[rk1[i]] - rd[i] <= re[rk2[i]]  # rt[i] == 3


satisfy(
    # computing starting times of orders
    [os[i] == rs[ot[i]] + sum(oh[j] * ow[j] for j in range(i) if ot[i] == ot[j]) for i in range(nOrders)],

    # computing lines of orders
    [ol[i] == rl[ot[i]] for i in range(nOrders)],

    # computing end times of recipes
    [re[i] == rs[i] + durations[i] for i in range(nRecipes)],

    Cumulative(
        origins=rs,
        lengths=durations,
        heights=1
    ) <= nLines,

    # each line has only one product at a time
    [
        Cumulative(
            origins=rs,
            lengths=durations,
            heights=[rl[i] == j for i in range(nRecipes)]
        ) <= 1 for j in range(nLines)
    ],

    # respecting flows
    [
        Cumulative(
            origins=rs,
            lengths=durations,
            heights=[recipes[i][j] for i in range(nRecipes)]
        ) <= flows[j] for j in range(nMinerals)
    ],

    # managing production rules
    [
        If(
            f[i],
            Then=production_rule(i)
        ) for i in range(nRules)
    ],

    # computing the make-span
    [re[i] <= m for i in range(nRecipes)]
)

minimize(
    Sum(f[i] == 0 for i in range(nRules)) * H + m
)

""" Comments
1) It seems that it would be simpler to change 0 and 1 for f
"""

# oe[i] is the end time of the ith order
# oe = VarArray(size=nOrders, dom=range(horizon))
