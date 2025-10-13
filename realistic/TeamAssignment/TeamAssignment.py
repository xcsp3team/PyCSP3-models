"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2022 Minizinc challenges.
The original MZN model was proposed by Erik Thörnbald (Uppsala University) - no licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  2-5-6.json

## Model
  constraints: AllDifferent, BinPacking, Maximum, Minimum, Sum

## Execution
  python TeamAssignment.py -data=<datafile.json>
  python TeamAssignment.py -data=<datafile.dzn> -parser=TeamAssignment_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn18, mzn22
"""

from pycsp3 import *

nTeams, nBoards, requests, rating, singleRequests, doubleRequests = data or load_json_data("2-5-6.json")

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
    BinPacking(
        partition=t,
        sizes=rating,
        loads=tr
    ),

    # computing the balance
    balance == Maximum(tr) - Minimum(tr),

    # computing the happiness
    happiness == 2 * Sum(t[i] == t[j] for i, j in doubleRequests) + Sum(t[i] == t[j] for i, j in singleRequests),

    # teams are different on each board
    [AllDifferent(t[b * nTeams: (b + 1) * nTeams]) for b in range(nBoards)],

    # tag(redundant)
    BinPacking(
        partition=t,
        sizes=1
    ) <= nBoards,

    # tag(symmetry-breaking)
    [t[i] == i for i in range(nTeams)]
)

maximize(
    1000 * happiness - balance
)

""" Comments
1) Now, we can indifferently write 
 Sum(t[i] == t[j] for i, j in doubleRequests) * 2
  or 
 2 * Sum(t[i] == t[j] for i, j in doubleRequests) 
 (in case the Sum generates the DummyConstraint 0 when doubleRequests is empty, this is ok)
"""
