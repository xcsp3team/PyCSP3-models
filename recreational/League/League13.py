"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  020-03-05.json

## Model
  constraints: Count, Sum, Maximum, Minimum

## Execution
  python League13.py -data=<datafile.json>
  python League13.py -data=<datafile.dzn> -parser=League_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  realistic, mzn13
"""

from pycsp3 import *

leagueSize, rankings, nationalities = data or load_json_data("020-03-05.json")

sr, sn = sorted(list(set(rankings))), sorted(list(set(nationalities))),
assert sr[0] == 0 and all(sr[i + 1] == sr[i] + 1 for i in range(len(sr) - 1))
assert sn[0] == 0 and all(sn[i + 1] == sn[i] + 1 for i in range(len(sn) - 1))

nRanks, nNationalities = len(sr), len(sn)
nPlayers = len(rankings)
nLeagues = (nPlayers + leagueSize - 1) // leagueSize

# sl[i] is the size of the ith league
sl = VarArray(size=nLeagues, dom=range(leagueSize - 1, leagueSize + 1))

# x[j] is the league of the jth player
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
    [Count(x, value=i) == sl[i] for i in range(nLeagues)],

    # managing ranks
    [
        [max_rank[i] == Maximum(rankings[j] * (x[j] == i) for j in range(nPlayers)) for i in range(nLeagues)],
        [min_rank[i] == Minimum(rankings[j] + 10000 * (x[j] != i) for j in range(nPlayers)) for i in range(nLeagues)],
        [diff_rank[i] == max_rank[i] - min_rank[i] for i in range(nLeagues)]
    ],

    # determining which nationality is present in each league
    [b[i][j] == Exist(x[p] == i for p in range(nPlayers) if nationalities[p] == j) for i in range(nLeagues) for j in range(nNationalities)],

    # determining the number of nationalities in each league
    [nn[i] == Sum(b[i]) for i in range(nLeagues)],

    # sorting result
    [
        Increasing(max_rank),
        Increasing(min_rank)
    ]
)

minimize(
    100 * Sum(diff_rank) - Sum(nn)
)

""" Comments
1) Simplifying code with Ordered constraints (compared to Minizinc):
  [max_rank[i] <= max_rank[i + 1] for i in range(nLeagues - 1)],
  [min_rank[i] <= min_rank[i + 1] for i in range(nLeagues - 1)]
  
2) This is a model in Minizinc 2013, after fixing some issues of 2012
"""
