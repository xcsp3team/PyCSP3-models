"""
Problem 039 on CSPLib.

A concert is to consist of nine pieces of music of different durations each involving a different combination of the five members of the orchestra.

## Data Example
  rs.json

## Model
  constraints: AllDifferent, Sum

## Execution
  python Rehearsal.py -data=<datafile.json>
  python Rehearsal.py -data=<datafile.json> -variant=bis

## Links
  - https://www.csplib.org/Problems/prob039/

## Tags
  realistic, csplib
"""

from pycsp3 import *

assert not variant() or variant("bis")

durations, playing = data or load_json_data("rs.json")

nPieces, nPlayers = len(durations), len(playing)

PP = [(i, j) for i in range(nPlayers) for j in range(nPieces)]

# p[j] is the piece played in slot j
p = VarArray(size=nPieces, dom=range(nPieces))

# s[i] is (the slot) when the ith player arrives (starts)
s = VarArray(size=nPlayers, dom=range(nPieces))

# e[i] is (the slot) when the ith player leaves (ends)
e = VarArray(size=nPlayers, dom=range(nPieces))

if not variant():

    satisfy(
        # all pieces of music must be played in some order
        AllDifferent(p),

        # a player must be present when a piece of music requires him/her
        [
            If(
                playing[i][p[j]],
                Then=[s[i] <= j, j <= e[i]]
            ) for i, j in PP
        ]
    )

    minimize(
        # minimizing the waiting time of players (i.e. without playing)
        Sum(durations[p[j]] * conjunction(playing[i][p[j]] == 0, s[i] <= j, j <= e[i]) for i, j in PP)
    )

elif variant("bis"):

    # ep[i][j] is 1 iff the ith player must effectively play in the jth slot
    ep = VarArray(size=[nPlayers, nPieces], dom={0, 1})

    satisfy(
        # all pieces of music must be played in some order
        AllDifferent(p),

        # determining when players must effectively play
        [ep[i][j] == playing[i][p[j]] for i, j in PP],

        # a player must be present when a piece of music requires him/her
        [
            If(
                ep[i][j],
                Then=[s[i] <= j, j <= e[i]]
            ) for i, j in PP
        ]
    )

    minimize(
        # minimizing the waiting time of players (i.e. without playing)
        Sum(durations[p[j]] * conjunction(ep[i][j] == 0, s[i] <= j, j <= e[i]) for i, j in PP)
    )

""" Comments
1) the first model variant is very compact. The second model variant explicitly introduces some auxiliary variables
   which, to som respect, allows a better control of the generated instances. Here, however, the outputs  are not
   so different for this problem.

2) we cannot currently write: (a[p] <= i <= b[p]) (this is technically not obvious to handle that, and even seems almost impossible)

3) Note that (the output may be slightly different):
  Then=[s[i] <= j, j <= e[i]]
can also be written :
  Then=both(s[i] <= j, j <= e[i])
or :
  Then=(s[i] <= j) & (j <= e[i])
"""
