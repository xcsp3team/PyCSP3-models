"""
Soccer Computational Problem (Position in Ranking Problem).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2020 Minizinc challenges.
The original MZN model was proposed by Robinson Duque, Alejandro Arbelaez, and Juan Francisco Díaz.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  22-12-22-5.json

## Model
  constraints: AllDifferent, Sum, Table

## Execution
  python Soccer.py -data=<datafile.json>
  python Soccer.py -data=<datafile.dzn> -parser=Soccer_ParserZ.py

## Links
  - https://www.aimsciences.org/article/doi/10.3934/jimo.2018109
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn18, mzn20
"""

from pycsp3 import *

games, iPoints, positions = data
nGames, nTeams, nPositions = len(games), len(iPoints), len(positions)

pt = [0, 1, 3]

lb_score = min(iPoints[i] + sum(min(pt) for j in range(nGames) if i in games[j]) for i in range(nTeams))
ub_score = max(iPoints[i] + sum(max(pt) for j in range(nGames) if i in games[j]) for i in range(nTeams))

# points[j][0] and points[j][1] are the points for the two teams (indexes 0 and 1) of the jth game
points = VarArray(size=[nGames, 2], dom=pt)

# score[i] is the final score of the ith team
score = VarArray(size=nTeams, dom=range(lb_score, ub_score + 1))

# fp[i] is the final position of the ith team
fp = VarArray(size=nTeams, dom=range(1, nTeams + 1))

# bp[i] is the best possible position of the ith team
bp = VarArray(size=nTeams, dom=range(1, nTeams + 1))

# wp[i] is the worst possible position of the ith team
wp = VarArray(size=nTeams, dom=range(1, nTeams + 1))

satisfy(
    # assigning rights points for each game
    [
        (points[j][0], points[j][1]) in {
            (0, 3),
            (1, 1),
            (3, 0)
        } for j in range(nGames)
    ],

    # computing final points
    [score[i] - Sum(points[j][0 if i == games[j][0] else 1] for j in range(nGames) if i in games[j]) == iPoints[i] for i in range(nTeams)],

    # computing worst positions (the number of teams with greater total points)
    [wp[i] == Sum(score[j] >= score[i] for j in range(nTeams)) for i in range(nTeams)],

    # computing best positions (from worst positions and the number of teams with equal points)
    [bp[i] == wp[i] - Sum(score[j] == score[i] for j in range(nTeams) if i != j) for i in range(nTeams)],

    # bounding final positions
    (
        (
            fp[i] >= bp[i],
            fp[i] <= wp[i]
        ) for i in range(nTeams)
    ),

    # ensuring different positions
    AllDifferent(fp),

    # applying rules from specified positions
    (
        (
            fp[i] == p,
            Sum(score[j] > score[i] for j in range(nTeams) if j != i) < p,
            Sum(score[j] < score[i] for j in range(nTeams) if j != i) <= nTeams + 1 - p
        ) for i, p in positions
    )
)

""" Comments
1) We can now write iPoints[i] + Sum(...) but it introduces auxiliary variables 
 [iPoints[i] + Sum(points[j][0] if i == games[j][0] else points[j][1] for j in range(numberOfGames) if i in games[j]) == score[i] for i in range(n)]
2) Warning: length(games) in Minizinc returns the number of elements in the array and not the number of rows.
"""
