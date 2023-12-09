"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2022 Minizinc challenges.
The MZN model was proposed by Erik Thörnbald (Uppsala University).
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  2-5-6.json

## Model
  constraints: AllDifferent, BinPacking, Maximum, Minimum, Sum

## Execution
  python TeamAssignment.py -data=<datafile.json>
  python TeamAssignment.py -data=<datafile.dzn> -parser=TeamAssignment_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  real, mzn18, mzn22
"""

from pycsp3 import *

nTeams, nBoards, requests, rating, singleRequests, doubleRequests = data
nPlayers = nTeams * nBoards

# t[i] is the team of the ith player
t = VarArray(size=nPlayers, dom=range(nTeams))

# tr[i] is the team rating of the ith team
tr = VarArray(size=nTeams, dom=range(nBoards * max(rating) + 1))

# the balance of the team ratings
balance = Var(dom=range(nBoards * max(rating) + 1))

# the global happiness wrt requests
happiness = Var(dom=range(requests + 1))

satisfy(
    # computing team ratings
    BinPacking(t, sizes=rating, loads=tr),

    # computing the balance
    balance == Maximum(tr) - Minimum(tr),

    # computing the happiness
    happiness == 2 * Sum(t[i] == t[j] for i, j in doubleRequests) + Sum(t[i] == t[j] for i, j in singleRequests),

    # teams are different on each board
    [AllDifferent(t[b * nTeams: (b + 1) * nTeams]) for b in range(nBoards)],

    # tag(redundant-constraint)
    BinPacking(t, sizes=1) <= nBoards,

    # tag(symmetry-breaking)
    [t[i] == i for i in range(nTeams)]
)

maximize(
    1000 * happiness - balance
)
