"""
Radio Link Frequency Assignment.

## Data Example
  graph-01.json

## Model
  constraints: Maximum, NValues, Sum

## Execution
  python RLFAP.py -data=<datafile.json> -variant=card
  python RLFAP.py -data=<datafile.json> -variant=span
  python RLFAP.py -data=<datafile.json> -variant=max

## Links
  - https://link.springer.com/article/10.1023/A:1009812409930
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
"""

from pycsp3 import *

assert variant("card") or variant("span") or variant("max")

domains, variables, constraints, interference_costs, mobility_costs = data or load_json_data("graph-01.json")

assert all((v is None) == (mob is None) for (_, v, mob) in variables)

n = len(variables)

# f[i] is the frequency of the ith radio link
f = VarArray(size=n, dom=lambda i: domains[variables[i].domain])

satisfy(
    # managing pre-assigned frequencies
    [f[i] == v for i, (_, v, _) in enumerate(variables) if v is not None and not variant("max")],

    # hard constraints on radio-links
    [
        Match(
            op,
            Cases={
                "=": abs(f[i] - f[j]) == k,
                ">": abs(f[i] - f[j]) > k,
            }
        ) for (i, j, op, k, wgt) in constraints if not variant("max") or wgt == 0
    ]
)

if variant("span"):
    minimize(
        # minimizing the largest frequency
        Maximum(f)
    )
elif variant("card"):
    minimize(
        # minimizing the number of used frequencies
        NValues(f)
    )
elif variant("max"):
    minimize(
        # minimizing the sum of violation costs
        Sum((f[i] != v) * mobility_costs[mob] for i, (_, v, mob) in enumerate(variables) if v is not None)
        + Sum((abs(f[i] - f[j]) != k if op == "=" else abs(f[i] - f[j]) <= k) * interference_costs[wgt] for (i, j, op, k, wgt) in constraints if wgt > 0)
    )

""" Comments
1) One could write:
  expr(op, abs(f[i] - f[j]), k) for (i, j, op, k, wgt) in constraints if not (variant("max") and wgt)]
  as expr allows us to build an expression (constraint) with an operator given as first parameter (possibly, a string)
  It could also have been written: abs(f[i] - f[j]) == k if op == "=" else abs(f[i] - f[j]) > k
2) The new way oif posting the objective function for variant "max" is seems better (for solving) than:
  Sum(ift(f[i] == v, 0, mobilityCosts[mob]) for i, (_, v, mob) in enumerate(variables) if v and mob)
  + Sum(ift(expr(op, abs(f[i] - f[j]), k), 0, interferenceCosts[wgt]) for (i, j, op, k, wgt) in constraints if wgt)
"""
