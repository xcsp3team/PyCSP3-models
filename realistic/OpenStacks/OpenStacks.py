"""

## Data Example
  pb-20-20-1.json

## Model
  There are two variants of this model.

  constraints: AllDifferent, Maximum, Minimum, Sum, Table

## Execution
  python OpenStacks.py -data=<datafile.json> -variant=m1
  python OpenStacks.py -data=<datafile.json> -variant=m2

## Links
  - https://ipg.host.cs.st-andrews.ac.uk/challenge/

## Tags
  realistic, notebook
"""

from pycsp3 import *

assert variant("m1") or variant("m2")

orders = data or load_json_data("pb-20-20-1.json")

n, m = len(orders), len(orders[0])  # n orders (customers), m possible products
N, M = range(n), range(m)

if variant("m1"):
    def T1(v):
        return {(0, 0, 0)} | {(j, ANY, 1) for j in range(1, v)} | {(v, 0, 0), (v, 1, 1)}


    # p[j] is the period (time) of the jth product
    p = VarArray(size=m, dom=range(m))

    # np[i][j] is the number of products made at time j and required by customer i
    np = VarArray(size=[n, m], dom=lambda i, j: range(sum(orders[i]) + 1))

    # r[i][t] is 1 iff the product made at time t concerns customer i
    r = VarArray(size=[n, m], dom={0, 1})

    # o[i][t] is 1 iff the stack is open for customer i at time t
    o = VarArray(size=[n, m], dom={0, 1})

    satisfy(
        # all products are scheduled at different times
        AllDifferent(p),

        [
            orders[i][p[j]] == r[i][j]
            for i in N for j in M
        ],

        [
            np[i][j] == (r[i][j] if j == 0 else np[i][j - 1] + r[i][j])
            for i in N for j in M
        ],

        [
            (np[i][j], r[i][j], o[i][j]) in T1(sum(orders[i]))
            for i in N for j in M
        ],
    )

    minimize(
        # minimizing the number of stacks that are simultaneously open
        Maximum(Sum(o[:, t]) for t in range(m))
    )

elif variant("m2"):
    def T2(t):
        return {(ANY, te, 0) for te in range(t)} | {(ts, ANY, 0) for ts in range(t + 1, m)} | {(ts, te, 1) for ts in range(t + 1) for te in range(t, m)}


    # p[j] is the period (time) of the jth product
    p = VarArray(size=m, dom=range(m))

    # s[i] is the starting time of the ith stack
    s = VarArray(size=n, dom=range(m))

    # e[i] is the ending time of the ith stack
    e = VarArray(size=n, dom=range(m))

    # o[i][t] is 1 iff the ith stack is open at time t
    o = VarArray(size=[n, m], dom={0, 1})

    satisfy(
        # all products are scheduled at different times
        AllDifferent(p),

        # computing starting times of stacks
        [
            s[i] == Minimum(p[j] for j in M if orders[i][j])
            for i in N
        ],

        # computing ending times of stacks
        [
            e[i] == Maximum(p[j] for j in M if orders[i][j])
            for i in N
        ],

        # inferring when stacks are open
        [
            (s[i], e[i], o[i][t]) in T2(t)
            for i in N for t in M
        ],
    )

    minimize(
        # minimizing the number of stacks that are simultaneously open
        Maximum(Sum(o[:, t]) for t in M)
    )

""" Comments
1) If we want explicitly the number of open stacks at time t, we write instead:
 # ns[t] is the number of open stacks at time t
 ns = VarArray(size=m, dom=range(m + 1))

 # computing the number of open stacks at any time
 [Sum(o[:, j]) == ns[j] for j in M]

 minimize (Maximum(ns))
"""
