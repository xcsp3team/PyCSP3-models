"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example

## Model
  constraints: Count, Sum

## Execution
  python MonitorPlacement.py -data=<datafile.json>
  python MonitorPlacement.py -data=<datafile.dzn> -parser=MonitorPlacement_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
"""

from pycsp3 import *

n, ends, routes, leaves, bi_comp = data
r, b = len(routes), len(bi_comp)

# x[i] is 1 if the ith node is a monitor
x = VarArray(size=n, dom={0, 1})

# y[k] is 1 if the kth route is a measurement path
y = VarArray(size=r, dom={0, 1})

satisfy(
    # for a route to be a monitor path, its endpoints needs to be both monitors
    [y[k] == both(x[i], x[j]) for k, (i, j) in enumerate(ends)],

    # each node in the network needs to be covered by at least one measurement path
    [Exist(y[k] for k in range(r) if i in routes[k]) for i in range(n)],

    # each node needs to be 1-identifiable, i.e. it needs to be distinguishable from each other node
    [Exist(y[k] for k in range(r) if (a in routes[k]) == (b not in routes[k])) for a, b in combinations(n, 2)],

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

"""
1) The third group is very long to build. Can we do something? (precomputing the list m seems to not to be useful)
"""

# from collections import defaultdict
#
# m = [[[] for _ in range(n)] for _ in range(n)]
# for a in range(n):
#     for b in range(a + 1, n):
#         for k in range(r):
#             if (a in routes[k] and b not in routes[k]) or (a not in routes[k] and b in routes[k]):
#                 m[a][b].append(k)
# print(m)
