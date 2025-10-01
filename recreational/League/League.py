"""
Make leagues for some games:
 - ranking should be close in each league
 - in a league, variety of country (where player comes from) is needed

## Data
  010-03-04.json

## Model
  constraints: AllDifferent, Maximum, Minimum, Sum, Table

## Execution
  python League.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic
"""

from pycsp3 import *

leagueSize, players = data or load_json_data("010-03-04.json")  # rankings and countries of players

rankings, countries = zip(*players)
nPlayers = len(players)
nLeagues = nPlayers // leagueSize + (1 if nPlayers % leagueSize != 0 else 0)
nFullLeagues = nLeagues if nPlayers % leagueSize == 0 else nLeagues - (leagueSize - nPlayers % leagueSize)
sizes = [leagueSize + (0 if i < nFullLeagues else -1) for i in range(nLeagues)]

# p[i][j] is the jth player of the ith league
p = VarArray(size=[nLeagues, leagueSize], dom=lambda i, j: range(nPlayers) if j < sizes[i] else None)

# r[i][j] is the ranking of the jth player of the ith league
r = VarArray(size=[nLeagues, leagueSize], dom=lambda i, j: rankings if j < sizes[i] else None)

# c[i][j] is the country of the jth player of the ith league
c = VarArray(size=[nLeagues, leagueSize], dom=lambda i, j: countries if j < sizes[i] else None)

T = {(i, rankings[i], countries[i]) for i in range(nPlayers)}

satisfy(
    # each player belongs to only one league
    AllDifferent(p),

    # linking players with their rankings and countries
    [(p[i][j], r[i][j], c[i][j]) in T for i in range(nLeagues) for j in range(sizes[i])]
)

minimize(
    # minimizing overall differences between highest and lowest rankings of players in leagues while paying attention to numbers of countries
    Sum(Maximum(r[i]) - Minimum(r[i]) for i in range(nLeagues)) * 100 - Sum(NValues(c[i]) for i in range(nLeagues))
)
