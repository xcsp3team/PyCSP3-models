"""
Variant of the prize collecting travelling salesman problem.
Here, a subtour is authorized (because there are negative costs).
See also the model in Minizinc

## Data Example
  25-5-5-9.json

## Model
  constraints: Count, Element, Sum, Table

## Execution
  python PrizeCollecting.py -data=<datafile.json>
  python PrizeCollecting.py -data=<datafile.dzn> -variant=table

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic
"""

from pycsp3 import *

n, prizes = data.n, data.prizes

# s[i] is the node that succeeds to the ith node in the tour (value i if unused)
s = VarArray(size=n, dom=range(n))

# p[i] is the position (starting at 0) of the ith node in the tour (-1 if unused)
p = VarArray(size=n, dom=range(-1, n))

# g[i] is the gain collected when going from the ith node to its successor in the tour
g = VarArray(size=n, dom=lambda i: set(prizes[i]))

satisfy(
    # node 0 is the first node of the tour
    p[0] == 0,

    # managing unused nodes
    [(p[i] != -1) == (s[i] != i) for i in range(n)],

    # each node appears at most once during the tour
    [Count(s, value=i) <= 1 for i in range(n)],

    # computing gains
    [prizes[i][s[i]] == g[i] for i in range(n)]
)

if not variant():
    satisfy(
        # linking variables from s and p
        If(
            s[i] != i, s[i] != 0,
            Then=p[s[i]] == p[i] + 1
        ) for i in range(n)
    )

elif variant("table"):
    def table(i):
        tbl = {(i,) + (ANY,) * n,  # i means "unused node", so this is not constraining (we use ANY)
               (0,) + (ANY,) * n}  # 0 means "last node", so this is not constraining (we use ANY)
        for j in range(1, n):
            if j != i:
                tbl |= {(j,) + tuple(v if k == j else v - 1 if k == i else ANY for k in range(n)) for v in range(1, n)}
        return tbl


    satisfy(
        # linking variables from s and p
        (s[i], *p) in table(i) for i in range(n)
    )

maximize(
    # maximizing the sum of collected gains
    Sum(g)
)

""" Comments
1) The short table is used to code the element constraints under condition
"""
