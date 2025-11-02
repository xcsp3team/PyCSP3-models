"""
In the new organization (since 2024) of the Football Champions's league, how many points a team can get in Phase 1 (playing 8 matches) while being ranked at a given position?

## Data Example
  2024.json

## Model
  constraints: Element, Sum, Table

## Execution
  python ChampionsLeague.py -data=<datafile.json>
  python ChampionsLeague.py -data=<datafile.json> -variant=strict
  python ChampionsLeague.py -data=[datafile.json,position=number]
  python ChampionsLeague.py -data=[datafile.txt,number] -parser=ChampionsLeague_Parser.py

## Links
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
"""

from pycsp3 import *

import random

assert not variant() or variant("strict")

if isinstance(data, int):
    random.seed(data)  # data is used as a seed
    schedule = [list(range(36)) for _ in range(8)]
    for row in schedule:
        random.shuffle(row)
    schedule = [[[row[i * 2], row[i * 2 + 1]] for i in range(len(row) // 2)] for row in schedule]
    position = 8
else:
    full_schedule, position = data or (load_json_data("phase1-2024.json"), 15)  # position is between 1 and 36)
    teams = sorted({team1 for day in full_schedule for (team1, _) in day})
    assert len(teams) == 36
    schedule = [[[teams.index(team1), teams.index(team2)] for (team1, team2) in day] for day in full_schedule]

nWeeks, nMatchesPerWeek, nTeams = len(schedule), len(schedule[0]), len(schedule[0]) * 2
W, T = range(nWeeks), range(nTeams)
assert nWeeks == 8 and nTeams == 36  # for the moment

WON, DRAWN, LOST = results = range(3)

# x[w][k] is the result of the kth match in the wth week
x = VarArray(size=[nWeeks, nMatchesPerWeek], dom=results)

# y[w][i] is the number of points won by the ith team in the wth week
y = VarArray(size=[nWeeks, nTeams], dom={0, 1, 3})

# z[i] is the number of points won by the ith team
z = VarArray(size=nTeams, dom=range(3 * nWeeks + 1))

# the target team that must be ranked at the specified position
target = Var(dom=range(nTeams))

# the number of points of the target team
z_target = Var(dom=range(3 * nWeeks + 1))

# the number of teams with a score better than the target team
better_target = Var(dom=range(nTeams))

# the number of teams with a score equal to the target team
equal_target = Var(dom=range(nTeams))

satisfy(
    # computing points won for every match
    [
        Table(
            scope=(x[w][k], y[w][i], y[w][j]),
            supports={(WON, 3, 0), (DRAWN, 1, 1), (LOST, 0, 3)}
        ) for w in W for k, (i, j) in enumerate(schedule[w])
    ],

    # computing the number of points of each team
    [z[i] == Sum(y[:, i]) for i in T],

    # tag(redundant)
    [Sum(y[w]).among(range(2 * nMatchesPerWeek, 3 * nMatchesPerWeek + 1)) for w in W],

    # linking the target team with  its score
    z[target] == z_target,

    # computing the number of teams that have a score better than the target team
    better_target == Sum(z[i] > z_target for i in T),

    # computing the number of teams that have a score equal to the target team (including itself)
    equal_target == Sum(z[i] == z_target for i in T),

    # the number of teams with a score better than the target team is less than the specified target position
    better_target < position,

    # the position of the target team must be compatible with the specified target position
    better_target == position - 1
    if variant("strict") else
    better_target + equal_target == position
)

maximize(
    # minimizing the number of points of the target team
    z_target
)

# better_target + equal_target == position if variant("strict") else better_target + equal_target >= position

""" Comments
1) Compilation example: python3 ChampionsLeague.py -data=[2024,12] -parser=ChampionsLeague_Parser.py
"""
