"""
Traveling Tournament Problem with Predefined Venues (TTPPV).
The problem consists of finding an optimal compact single round-robin schedule for a sport event.
Given a set of n teams, each team has to play against every other team exactly once.
In each round, a team plays either at home or away, however no team can play more than three consecutive times at home or away.
The sum of the traveling distance of each team has to be minimized.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
The venue of each game has already been decided.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  circ08bbal.json

## Model
  constraints: AllDifferent, Element, Regular, Sum

## Execution
  python TTP_PV.py -data=<datafile.json>
  python TTP_PV.py -data=<datafile.dzn> -parser=TTP_PV_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob068/models/
  - https://link.springer.com/article/10.1007/s10951-008-0097-1
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, csplib, mzn14, mzn17, mzn22
"""

from pycsp3 import *

nTeams, venues = data
nRounds = nTeams - 1
assert nTeams % 2 == 0, "an even number of teams is expected"

distances = cp_array([min(abs(v1 - v2), nTeams - abs(v1 - v2)) for v2 in range(nTeams)] for v1 in range(nTeams))


def automaton():
    qi, q01, q02, q03, q11, q12, q13 = states = "q", "q01", "q02", "q03", "q11", "q12", "q13"
    tr2 = [(qi, 0, q01), (qi, 1, q11), (q01, 0, q02), (q01, 1, q11), (q11, 0, q01), (q11, 1, q12), (q02, 1, q11), (q12, 0, q01)]
    tr3 = [(q02, 0, q03), (q12, 1, q13), (q03, 1, q11), (q13, 0, q01)]
    return Automaton(start=qi, final={q for q in states if q != qi}, transitions=tr2 + tr3)


A = automaton()

# o[i][k] is the opponent (team) of the ith team  at the kth round
o = VarArray(size=[nTeams, nRounds], dom=range(nTeams))

# h[i][k] is 1 iff the ith team plays at home at the kth round
h = VarArray(size=[nTeams, nRounds], dom={0, 1})

# t[i][k] is the travelled distance by the ith team at the kth round. An additional round is considered for returning home.
t = VarArray(size=[nTeams, nRounds + 1], dom=range(nTeams // 2 + 1))

satisfy(
    # ensuring predefined venues
    [venues[i][o[i][k]] == h[i][k] for i in range(nTeams) for k in range(nRounds)],

    # a team cannot play against itself
    [o[i][k] != i for i in range(nTeams) for k in range(nRounds)],

    # in round k, i plays j means j plays i
    [o[o[i][k]][k] == i for i in range(nTeams) for k in range(nRounds)],

    # each team plays once against all other teams
    [AllDifferent(row) for row in o],

    # at each round, opponents are all different  tag(redundant-constraints)
    [AllDifferent(col) for col in columns(o)],

    # at most 3 consecutive games at home, or consecutive games away
    [h[i] in A for i in range(nTeams)],

    # tag(symmetry-breaking)
    o[0][0] < o[0][-1],

    # computing travelled distances wrt venues of current and next-round games
    [
        [
            (
                If(h[i][0] == 1, Then=t[i][0] == 0),
                If(h[i][0] != 1, Then=t[i][0] == distances[i][o[i][0]])
            ) for i in range(nTeams)
        ],

        [
            (
                If(h[i][k] == 1, h[i][k + 1] == 1, Then=t[i][k + 1] == 0),
                If(h[i][k] != 1, h[i][k + 1] == 1, Then=t[i][k + 1] == distances[o[i][k]][i]),
                If(h[i][k] == 1, h[i][k + 1] != 1, Then=t[i][k + 1] == distances[i][o[i][k + 1]]),
                If(h[i][k] != 1, h[i][k + 1] != 1, Then=t[i][k + 1] == distances[o[i][k]][o[i][k + 1]])
            ) for i in range(nTeams) for k in range(nRounds - 1)
        ],

        [
            (
                If(h[i][-1] == 1, Then=t[i][-1] == 0),
                If(h[i][-1] != 1, Then=t[i][-1] == distances[o[i][-1]][i])
            ) for i in range(nTeams)
        ]
    ]
)

minimize(
    # minimizing summed up travelled distance
    Sum(t)
)
