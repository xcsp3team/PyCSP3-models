"""
In a 14-team league, form 2 divisions which hold a SRRT (Single Round-Robin Tournament):
  - each 7-team division must hold a SRRT to start the season
  - this must be followed by two SRRTs between the entire league, the second SRRT being a mirror of the first
  - there must be a minimum number of breaks in the schedule (home-home pair or away-away pair)
  - each team has one bye during the season (to occur during the divisional RRT)
  - at no point during the season can the number of home and away games played by a team differ by more than 1
  - any pair of teams must have consecutive meetings occur at different venues (Alternative Venue Requirement)
  - each division must have 3 pairs of complementary schedules

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2016/2018/2023 Minizinc challenges.
The MZN model was proposed by Jeff Larson and Mats Carlsson, and described in the papers mentioned below.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  handball01.json

## Model
  constraints: AllDifferent, Cardinality, Channel, Count, Element, Regular, Sum, Table

## Execution
  python Elitserien.py -data=<datafile.json>
  python Elitserien.py -data=<datafile.dzn> -parser=Elitserien_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0377221716309584?via%3Dihub
  - https://link.springer.com/chapter/10.1007/978-3-319-07046-9_11
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn14, mzn16, mzn18, mzn23
"""

from pycsp3 import *

noHome, group1, group2, derbys, complementaryPairs = data
derbyPeriod = [39 - p if p > 19 else p for (_, p) in derbys]  # p for period
nDerbys = len(derbys)

nTeams, nPeriods = 14, 20
DivisionSize = 7
north_teams, south_teams = range(DivisionSize), range(DivisionSize, 2 * DivisionSize)
tour1, tour2 = range(7), range(7, 20)

AWAY, BYE, HOME = values = 1, 2, 3

INIT, B_1, A_1, H_1, A_2, H_2, AB_2, HB_2, A_3, H_3, AB_3, HB_3, A_4, H_4, AB_4, HB_4, A_5, H_5, AB_5, HB_5, A_6, H_6, AB_6, \
    HB_6, AB_7, HB_7, AB_8, HB_8, AB_9, HB_9, AB_20, HB_20 = states = Automaton.states_for(range(1, 33))

t = [[A_1, B_1, H_1],  # INIT, start state
     [AB_2, 0, HB_2],  # B_1
     [0, AB_2, H_2],  # A_1
     [A_2, HB_2, 0],  # H_1
     [0, AB_3, H_3],  # A_2
     [A_3, HB_3, 0],  # H_2
     [0, 0, HB_3],  # AB_2
     [AB_3, 0, 0],  # HB_2
     [0, AB_4, H_4],  # A_3
     [A_4, HB_4, 0],  # H_3
     [0, 0, HB_4],  # AB_3
     [AB_4, 0, 0],  # HB_3
     [0, AB_5, H_5],  # A_4
     [A_5, HB_5, 0],  # H_4
     [0, 0, HB_5],  # AB_4
     [AB_5, 0, 0],  # HB_4
     [0, AB_6, H_6],  # A_5
     [A_6, HB_6, 0],  # H_5
     [0, 0, HB_6],  # AB_5
     [AB_6, 0, 0],  # HB_5
     [0, AB_7, 0],  # A_6
     [0, HB_7, 0],  # H_6
     [0, 0, HB_7],  # AB_6
     [AB_7, 0, 0],  # HB_6
     [0, 0, HB_8],  # AB_7
     [AB_8, 0, 0],  # HB_7
     [0, 0, HB_9],  # AB_8, accept state
     [AB_9, 0, 0],  # HB_8, accept state
     [AB_20, 0, HB_8],  # AB_9
     [AB_8, 0, HB_20],  # HB_9
     [0, 0, HB_20],  # AB_20, accept state
     [AB_20, 0, 0]  # HB_20, accept state
     ]

transitions = [(s, v, Automaton.q(0) if isinstance(t[i][j], int) else t[i][j]) for i, s in enumerate(states) for j, v in enumerate(values)]
A = Automaton(start=INIT, final=[AB_8, HB_8, AB_20, HB_20], transitions=transitions)

# whr[t][p] is where is playing team t at period p
whr = VarArray(size=[nTeams, nPeriods], dom={AWAY, BYE, HOME})

# opp[t][p] is the opponent (team) of team t at period p
opp = VarArray(size=[nTeams, nPeriods], dom=range(nTeams))

# brk[t] is the number of breaks of team t
brk = VarArray(size=nTeams, dom=range(20))

# row[t] is the row of the team t in the template
row = VarArray(size=nTeams, dom=range(nTeams))

# csc[t] is 1 if team t has a complementary schedule with respect to team t+1   tag(symmetry-breaking)
csc = VarArray(size=nTeams - 1, dom={0, 1})

satisfy(
    # assigning divisions
    [
        [row[t] in north_teams for t in group1],
        [row[t] in south_teams for t in group2]
    ],

    # handling derbys
    [
        [
            Exist(
                both(
                    opp[row[t]][derbyPeriod] == row[u],
                    opp[row[u]][derbyPeriod] == row[t]
                ) for t, u in combinations(derbySet, 2)
            ) for derbySet, derbyPeriod in derbys if len(derbySet) == 3
        ],

        [
            (
                Exist([row[u] for u in derbySet if u != t], value=opp[row[t]][derbyPeriod]),
                Exist([opp[row[u]][derbyPeriod] for u in derbySet if u != t], value=row[t])
            ) for derbySet, derbyPeriod in derbys if len(derbySet) == 4 for t in derbySet
        ]
    ],

    # managing complementary schedules
    [
        (
            brk[row[t]] == brk[row[u]],
            [whr[row[t]][p] != whr[row[u]][p] for p in range(nPeriods)]
        ) for t, u in complementaryPairs
    ],

    # first round-robin tournament
    [
        [opp[t][p] in north_teams for p in tour1 for t in north_teams],
        [opp[t][p] in south_teams for p in tour1 for t in south_teams]
    ],

    # computing breaks (2)
    [brk[t] == Sum(p * (whr[t][p - 1] == whr[t][p]) for p in {9, 11, 13, 15, 17, 19}) for t in range(nTeams)],

    # constraining where teams can play in sequence (4)
    [whr[t] in A for t in range(nTeams)],

    # RRT (5)
    [Channel(opp[:, p]) for p in range(nPeriods)],

    # RRT (6)
    [
        [AllDifferent(opp[t][tour1]) for t in range(nTeams)],
        [AllDifferent(opp[t][tour2]) for t in range(nTeams)]
    ],

    # ensuring the compatibility of venues how (where) opponents play (7)
    [whr[opp[t][p]][p] + whr[t][p] == AWAY + HOME for p in range(nPeriods) for t in range(nTeams)],

    # alternative venue requirements (1) (8)
    [AllDifferent(3 * opp[t][p] + whr[t][p] for p in range(nPeriods)) for t in range(nTeams)],

    # tag(redundant-constraints)
    [
        # considering the consequence of Bye (3)
        [(opp[t][p] == t) == (whr[t][p] == BYE) for t in range(nTeams) for p in range(nPeriods)],

        # exactly six aligned breaks per division (10)
        [
            [Sum(brk[t] > 0 for t in north_teams) == 6],
            [Sum(brk[t] > 0 for t in south_teams) == 6]
        ],

        # exactly two occurrences of every break period (12)
        Cardinality(brk, occurrences={v: 2 for v in (0, 9, 11, 13, 15, 17, 19)})
    ],

    # tag(symmetry-breaking)
    [
        # setting bye periods (15)
        [
            [whr[t][t] == BYE for t in north_teams],
            [whr[t + DivisionSize][t] == BYE for t in north_teams]
        ],

        # each division must have 3 pairs of complementary schedules (16)
        [
            [
                csc[t] == both(
                    brk[t] == brk[t + 1],
                    NotExist(whr[t][p] == whr[t + 1][p] for p in range(nPeriods))
                ) for t in range(nTeams - 1) if t != 6
            ],
            [csc[t1] | csc[t2] for t1, t2 in [(0, 1), (2, 3), (4, 5), (7, 8), (9, 10), (11, 12)]]
        ],

        # teams 1, 3, 5, 8, 10, 12 must have breaks (17)
        [brk[t] > 0 for t in {1, 3, 5, 8, 10, 12}],

        # the first row and the first column are complementary for each division (18)
        [
            [whr[t][0] + whr[0][t] == AWAY + HOME for t in north_teams],
            [whr[t + DivisionSize][0] + whr[DivisionSize][t] == AWAY + HOME for t in north_teams]
        ]
    ]
)

minimize(
    Sum(whr[row[t]][p] == HOME for t in range(nTeams) for p in range(nPeriods) if noHome[t][p] == 1)
    + Sum(whr[row[t]][39 - p] == AWAY for t in range(nTeams) for p in range(20, 33) if noHome[t][p] == 1)
)

"""
1) Groups of constraints (9), (11), (13) and (14) are in comments in the original model (so, not introduced here)

2) [AllDifferent(opp[t][tour2]) for t in range(nTeams)]
 is more compact to write than:
   [AllDifferent(opp[t][p] for p in tour2) for t in range(nTeams)]
   
3) the array teams is not really useful, and so isd put in comments:
   teams = VarArray(size=nTeams, dom=range(nTeams))  # the inverse of row
   Channel(row, teams),

4) Note that
  [Exist([row[u] for u in derbySet if u != t], value=opp[row[t]][derbyPeriod])
    for derbySet, derbyPeriod in derbys if len(derbySet) == 4 for t in derbySet],
 
  [Exist([opp[row[u]][derbyPeriod] for u in derbySet if u != t], value=row[t])
    for derbySet, derbyPeriod in derbys if len(derbySet) == 4 for t in derbySet]

can be replaced by:

  [opp[row[t]][derbyPeriod] in [row[u] for u in derbySet if u != t]
    for derbySet, derbyPeriod in derbys if len(derbySet) == 4 for t in derbySet],

  [row[t] in [opp[row[u]][derbyPeriod] for u in derbySet if u != t]
    for derbySet, derbyPeriod in derbys if len(derbySet) == 4 for t in derbySet]
"""
