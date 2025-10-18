"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example

## Model
  constraints: Count, Sum

## Execution
  python MonitorPlacement.py -data=<datafile.json>
  python MonitorPlacement.py -data=<datafile.dzn> -parser=MonitorPlacement_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
"""

from pycsp3 import *

# print(data)

n, ends, routes, leaves, bi_comp = data

nRoutes = len(routes)


def build_identifiable_sets():
    complementary_routes = [[i for i in range(n) if i not in route] for route in routes]

    m = [[[] for _ in range(n)] for _ in range(n)]
    for k in range(nRoutes):
        for a in routes[k]:
            for b in complementary_routes[k]:
                if a < b:
                    m[a][b].append(k)
                else:
                    m[b][a].append(k)
    return m


identifiable_sets = build_identifiable_sets()

# x[i] is 1 if the ith node is a monitor
x = VarArray(size=n, dom={0, 1})

# y[k] is 1 if the kth route is a measurement path
y = VarArray(size=nRoutes, dom={0, 1})

satisfy(
    # for a route to be a monitor path, its endpoints needs to be both monitors
    [y[k] == both(x[i], x[j]) for k, (i, j) in enumerate(ends)],

    # each node in the network needs to be covered by at least one measurement path
    [Exist(y[k] for k in range(nRoutes) if i in routes[k]) for i in range(n)],

    # each node needs to be 1-identifiable, i.e. it needs to be distinguishable from each other node
    [Exist(y[k] for k in identifiable_sets[a][b]) for a, b in combinations(n, 2)],

    # tag(redundant)
    [
        # some independent nodes need to be monitors
        [x[i] == 1 for i in leaves],

        # ensuring that each bi-connected component with only one articulation point contains at least one monitor to cover its nodes
        [Exist(x[bic]) for bic in bi_comp]
    ]
)

minimize(
    # minimizing the number of monitors
    Sum(x)
)

""" Comments
1) One could be tempted to write something like that for the third group: 
 [Exist(y[k] for k in range(r) if (a in routes[k]) == (b not in routes[k])) for a, b in combinations(n, 2)],
  but this is very long to build (this is why we have precomputed sets)
"""
