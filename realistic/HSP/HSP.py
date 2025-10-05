"""
We consider a facility with a single handling resource (a hoist).
The hoist has to perform a sequence of moves in order to accomplish a set of jobs, with varying
processing requirements, while satisfying processing and transport resource constraints.
The objective is to determine a feasible schedule (i.e., a sequence) that minimizes the total processing
time of a set of jobs (i.e., the makespan), while, at the same time, satisfying surface treatment constraints

## Data (example)
  10405.json

## Model
  Three variants compute differently dip durations:
  - a main variant involving logical constraints
  - a variant 'aux' involving auxiliary variables and logical constraints
  - a variant 'table' involving auxiliary variables and table constraints

  constraints: AllDifferent, Maximum, NoOverlap, Table

## Execution
  python HSP.py -data=<datafile.json>
  python HSP.py -data=<datafile.json> -variant=aux
  python HSP.py -data=<datafile.json> -variant=table

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054815002373
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

assert not variant() or variant("aux") or variant("table")

intervals, ld, ud = data or load_json_data("10405.json")  # loaded and unloaded time for one move (from one tank to one of its successors)

min_dips, max_dips = zip(*intervals)  # min and max dip durations
nTanks = len(intervals) + 1
horizon = sum(min_dips) + ld * nTanks + ud * nTanks + 1

# t[i] is the time when the product is picked from the ith tank
t = VarArray(size=nTanks, dom=range(horizon - ld - ud))

# o[i] is the order in which the picking operation of the ith tank is executed
o = VarArray(size=nTanks, dom=range(nTanks))

# d[i] is the dip duration in the ith tank (plus ld)
d = VarArray(size=nTanks, dom=lambda i: range(min_dips[i - 1] + ld, max_dips[i - 1] + 1 + ld) if i != 0 else {0})  # i-1 because of special tank 0

# time of the cycle
z = Var(range(nTanks * (ld + ud), horizon))


def duration_limit(i, j, delta):
    assert i < j
    return ld + ud * (abs(j - i) + delta)


satisfy(
    # the first operation corresponds to starting the cycle by putting a product in the first tank
    [
        t[0] == 0,
        o[0] == 0
    ],

    # taking into account the time of going back to tank 0
    [t[i] <= horizon - ld - (i + 1) * ud for i in range(1, nTanks)],

    # operations are executed in some order
    AllDifferent(o),

    # order of picking operations must be compatible with their picking times
    [(o[i] < o[j]) == (t[i] < t[j]) for i, j in combinations(nTanks, 2)],

    # ensuring a minimal duration between any two tanks
    NoOverlap(
        origins=t,
        lengths=ld + min(ud, min(min_dips))
    ),

    # computing the time of the cycle
    z == Maximum(t[i] + ld + (i + 1) * ud for i in range(1, nTanks)),

    # ensuring a duration limit between any two tanks
    [
        (
            If(
                o[j] - o[i] == 1,
                Then=t[j] - t[i] >= duration_limit(i, j, -1)
            ),
            If(
                o[i] - o[j] == 1,
                Then=t[i] - t[j] >= duration_limit(i, j, +1)
            )
        ) for i, j in combinations(nTanks, 2)
    ]
)

if not variant():
    satisfy(
        # computing the dip duration of each product
        d[i] == ift(o[i] < o[i - 1], z + t[i] - t[i - 1], t[i] - t[i - 1]) for i in range(1, nTanks)
    )
else:
    assert variant() in ("aux", "table")

    # g[i] is the gap (distance) between t[i] and t[i+1]
    g = VarArray(size=nTanks - 1, dom=range(-horizon, horizon))

    satisfy(
        # reducing the domain of auxiliary variables
        (
            g[i] < horizon - ld - (i + 2) * ud,
            g[i] > -horizon + ld + (i + 2) * ud
        ) for i in range(1, nTanks - 1)
    )

    if variant("aux"):

        satisfy(
            # computing the gap/distance between the picking time concerning two successive tanks
            [g[i] == t[i + 1] - t[i] for i in range(nTanks - 1)],

            # computing the dip duration of each product
            [d[i] == ift(g[i - 1] < 0, z + g[i - 1], g[i - 1]) for i in range(1, nTanks)]
        )

    elif variant("table"):

        T1 = [(v2 - v1, v2, v1) for v2 in t[2].dom for v1 in t[1].dom if v2 - v1 in g[1].dom]
        T2 = [[(vt + vg if vg < 0 else vg, vg, vt) for vg in g[i - 1].dom for vt in z.dom if (vt + vg if vg < 0 else vg) in d[i].dom] for i in range(1, nTanks)]

        satisfy(
            # computing the gap/distance between two successive tanks
            [(g[i], t[i + 1], t[i]) in T1 for i in range(nTanks - 1)],

            # computing the dip duration of each product
            [(d[i], g[i - 1], z) in T2[i - 1] for i in range(1, nTanks)]
        )

minimize(
    #  minimizing the time of the cycle
    z
)

""" Comments
1) It is possible to compute a lower bound when defining the objective variable z
2) It is possible to reduce the domain of variables g at construction time. useful?
   For example:  g = VarArray(size=nTanks - 1,
                       dom=range(-horizon + ld + 2 * ud, horizon - ld - 2 * ud))  
   It is even possible to do better     
3) The basic variant is not efficient
"""
