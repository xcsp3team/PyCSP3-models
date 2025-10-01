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

vr_sizes, ve_sizes = data or load_json_data("04.json")

nVisitors, nVisitees = sum(vr_sizes), sum(ve_sizes)
assert nVisitors >= nVisitees, "The number of visitors must be greater than the number of visitees"
if nVisitors - nVisitees > 0:
    ve_sizes.append(nVisitors - nVisitees)  # an artificial group with dummy visitees is added
nWeeks = len(vr_sizes)

V, W = range(nVisitors), range(nWeeks)

Tvr = {(i, sum(vr_sizes[:i]) + j) for i, size in enumerate(vr_sizes) for j in range(size)}
Tve = {(i, sum(ve_sizes[:i]) + j) for i, size in enumerate(ve_sizes) for j in range(size)}

# vr[i][w] is the visitor for the ith visitee at week w
vr = VarArray(size=[nVisitors, nWeeks], dom=range(nVisitors))

# ve[i][w] is the visitee for the ith visitor at week w
ve = VarArray(size=[nVisitors, nWeeks], dom=range(nVisitors))

# vrg[i][w] is the visitor group for the ith visitee at week w
vrg = VarArray(size=[nVisitors, nWeeks], dom=range(len(vr_sizes)))

# veg[i][w] is the visitee group for the ith visitor at week w
veg = VarArray(size=[nVisitors, nWeeks], dom=range(len(ve_sizes)))

satisfy(
    # each week, all visitors must be different
    [AllDifferent(col) for col in columns(vr)],

    # each week, all visitees must be different
    [AllDifferent(col) for col in columns(ve)],

    # the visitor groups must be different for each visitee
    [AllDifferent(row) for row in vrg],

    # the visitee groups must be different for each visitor
    [AllDifferent(row) for row in veg],

    # channeling arrays vr and ve, each week
    [Channel(vr[:, w], ve[:, w]) for w in W],

    # tag(symmetry-breaking)
    [
        LexIncreasing(vr, matrix=True),

        [Increasing(vr[nVisitees:nVisitors, w], strict=True) for w in W]
    ],

    # linking a visitor with its group
    [(vrg[i][w], vr[i][w]) in Tvr for i in range(nVisitors) for w in W],

    # linking a visitee with its group
    [(veg[i][w], ve[i][w]) in Tve for i in range(nVisitors) for w in W]
)

"""
1) Note that
 r[nVisitees:n, w]
   is a shortcut for:
 [r[i][w] for i in range(nVisitees, n)]
2) The symmetr-breaking constraints are discarded for the mini-tracks of the competition
"""
