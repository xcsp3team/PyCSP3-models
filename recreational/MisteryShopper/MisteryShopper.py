"""
See description on CSPLib.

## Data Example
  04.json

## Model
  constraints: AllDifferent, Channel, Lex, Table

## Execution:
  python MisteryShopper.py -data=<datafile.json>
  python MisteryShopper.py -parser=MisteryShopper_Random.py <number> <number> <number> <number> <number>

## Links
 - https://www.csplib.org/Problems/prob004
 - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  recreational, csplib, xcsp24
"""

from pycsp3 import *

vr_sizes = data.visitorGroups  # vr_sizes[i] gives the size of the ith visitor group
ve_sizes = data.visiteeGroups  # ve_sizes[i] gives the size of the ith visitee group

nVisitors, nVisitees = sum(vr_sizes), sum(ve_sizes)
assert nVisitors >= nVisitees, "The number of visitors must be greater than the number of visitees"
if nVisitors - nVisitees > 0:
    ve_sizes.append(nVisitors - nVisitees)  # an artificial group with dummy visitees is added
n, nWeeks = nVisitors, len(vr_sizes)

vr_table = {(i, sum(vr_sizes[:i]) + j) for i, size in enumerate(vr_sizes) for j in range(size)}
ve_table = {(i, sum(ve_sizes[:i]) + j) for i, size in enumerate(ve_sizes) for j in range(size)}

# r[i][w] is the visitor for the ith visitee at week w
r = VarArray(size=[n, nWeeks], dom=range(n))

# e[i][w] is the visitee for the ith visitor at week w
e = VarArray(size=[n, nWeeks], dom=range(n))

# rg[i][w] is the visitor group for the ith visitee at week w
rg = VarArray(size=[n, nWeeks], dom=range(len(vr_sizes)))

# eg[i][w] is the visitee group for the ith visitor at week w
eg = VarArray(size=[n, nWeeks], dom=range(len(ve_sizes)))

satisfy(
    # each week, all visitors must be different
    [AllDifferent(col) for col in columns(r)],

    # each week, all visitees must be different
    [AllDifferent(col) for col in columns(e)],

    # the visitor groups must be different for each visitee
    [AllDifferent(row) for row in rg],

    # the visitee groups must be different for each visitor
    [AllDifferent(row) for row in eg],

    # channeling arrays vr and ve, each week
    [Channel(r[:, w], e[:, w]) for w in range(nWeeks)],

    # tag(symmetry-breaking)
    [
        LexIncreasing(r, matrix=True),

        [Increasing(r[nVisitees:n, w], strict=True) for w in range(nWeeks)]
    ],

    # linking a visitor with its group
    [(rg[i][w], r[i][w]) in vr_table for i in range(n) for w in range(nWeeks)],

    # linking a visitee with its group
    [(eg[i][w], e[i][w]) in ve_table for i in range(n) for w in range(nWeeks)]
)

"""
1) Note that
 r[nVisitees:n, w]
   is a shortcut for:
 [r[i][w] for i in range(nVisitees, n)]
2) The symmetr-breaking constraints are discarded for the mini-tracks of the competition
"""
