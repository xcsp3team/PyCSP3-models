"""
Make leagues for some games:
 - ranking should be close in each league
 - in a league, variety of country (where player comes from) is needed

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data
  020-03-05.json

## Model
  constraints: Count, Maximum, Minimum, Sum

## Execution
  python League_z.py -data=<datafile.json>
  python League_z.py -data=<datafile.dzn> -parser=League_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
"""

from pycsp3 import *

leagueSize, rankings, nationalities = data or load_json_data("020-03-05.json")

sr, sn = sorted(set(rankings)), sorted(set(nationalities))
assert sr[0] == 0 and all(sr[i + 1] == sr[i] + 1 for i in range(len(sr) - 1))
assert sn[0] == 0 and all(sn[i + 1] == sn[i] + 1 for i in range(len(sn) - 1))

nRanks, nNationalities = len(sr), len(sn)
nPlayers = len(rankings)
nLeagues = (nPlayers + leagueSize - 1) // leagueSize

L, P = range(nLeagues), range(nPlayers)

# sl[i] is the size of the ith league
sl = VarArray(size=nLeagues, dom=range(leagueSize - 1, leagueSize + 1))

# x[p] is the league of player p
x = VarArray(size=nPlayers, dom=range(nLeagues))

max_rank = VarArray(size=nLeagues, dom=range(nRanks))

min_rank = VarArray(size=nLeagues, dom=range(nRanks))

diff_rank = VarArray(size=nLeagues, dom=range(nRanks))

# b[i][j] is 1 if the jth nationality is present in the ith league
b = VarArray(size=[nLeagues, nNationalities], dom={0, 1})

# nn[i] is the number of nationalities in the ith league
nn = VarArray(size=nLeagues, dom=range(leagueSize + 1))

satisfy(
    # computing the size of leagues
    [
        Count(
            within=x,
            value=i
        ) == sl[i] for i in L
    ],

    # managing ranks
    [
        [
            If(
                x[p] == i,
                Then=max_rank[i] >= rankings[p]
            ) for i in L for p in P
        ],
        [
            If(
                x[j] == i,
                Then=min_rank[i] <= rankings[j]
            ) for i in L for j in P
        ],
        [diff_rank[i] == max_rank[i] - min_rank[i] for i in L]
    ],

    # determining which nationality is present in each league
    [b[i][j] == Exist(x[p] == i for p in P if nationalities[p] == j) for i in L for j in range(nNationalities)],

    # determining the number of nationalities in each league
    [nn[i] == Sum(b[i]) for i in L],

    # tag(symmetry-breaking)
    [max_rank[i] <= max_rank[i + 1] for i in L[:-1]],

    # bad assumption from the original MZN model
    [diff_rank[i] > 0 for i in L]
)

minimize(
    Sum(diff_rank) * 10000 - Sum(nn)
)

""" Comments
1) we insert the last group to be coherent with the original model (from the 2012 competition)
Otherwise, it seems that this group must be discarded to solve the initial problem
"""
