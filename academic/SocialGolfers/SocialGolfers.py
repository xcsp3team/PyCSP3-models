"""
This is [Problem 010](https://www.csplib.org/Problems/prob010/) at CSPLib.

The coordinator of a local golf club has come to you with the following problem.
In their club, there are 32 social golfers, each of whom play golf once a week, and always in groups of 4.
They would like you to come up with a schedule of play for these golfers,
to last as many weeks as possible, such that no golfer plays in the same group as any other golfer on more than one occasion.
The problem can easily be generalized to that of scheduling groups of golfers over at most weeks, such
that no golfer plays in the same group as any other golfer twice (i.e. maximum socialisation is achieved).
For the original problem, the values of and are respectively 8 and 4.

## Data
  A triplet (n,s,w), where n is the number of groups, s the size of the groups and w the number of weeks.

## Model
  You can  find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/SocialGolfers/).

  There are 2 variants: a main one, and a variant '01' with additional variables

  constraints: Cardinality, Lex, Sum

## Execution
  python SocialGolfers.py -data=[number,number,number]
  python SocialGolfers.py -data=[number,number,number] -variant=cnt

## Links
  - https://en.wikipedia.org/wiki/Social_golfer_problem
  - https://en.wikipedia.org/wiki/Kirkman%27s_schoolgirl_problem
  - https://www.csplib.org/Problems/prob010/

## Tags
  academic, notebook, csplib
"""

from pycsp3 import *

nGroups, size, nWeeks = data or (4, 4, 5)  # size is the size of the groups
nPlayers = nGroups * size

# g[w][p] is the group admitting on week w the player p
g = VarArray(size=[nWeeks, nPlayers], dom=range(nGroups))

if not variant():
    satisfy(
        # ensuring that two players don't meet more than one time
        [
            If(
                g[w1][p1] == g[w1][p2],
                Then=g[w2][p1] != g[w2][p2]
            ) for w1, w2 in combinations(nWeeks, 2) for p1, p2 in combinations(nPlayers, 2)
        ]
    )

elif variant("cnt"):
    satisfy(
        # ensuring that two players don't meet more than one time
        [Sum(g[w][p1] == g[w][p2] for w in range(nWeeks)) <= 1 for p1, p2 in combinations(nPlayers, 2)]
    )

satisfy(
    # respecting the size of the groups
    [
        Cardinality(
            within=g[w],
            occurrences={i: size for i in range(nGroups)}
        ) for w in range(nWeeks)
    ],

    # tag(symmetry-breaking)
    [
        LexIncreasing(g, matrix=True),

        [g[0][p] == p // size for p in range(nPlayers)],

        [g[w][k] == k for k in range(size) for w in range(1, nWeeks)]
    ]
)

if nGroups == size and nGroups + 1 == nWeeks:
    satisfy(
        # tag(redundant)
        [
            [AllDifferent(g[1:, p * size:p * size + size], matrix=True) for p in range(1, nGroups)],

            [g[1][k] == k % size for k in range(size, nPlayers)]
        ]
    )

else:
    satisfy(
        # tag(redundant)
        [
            AllDifferent(g[w][p * size:p * size + size]) for w in range(1, nWeeks) for p in range(1, nGroups)
        ]
    )

"""
1) Some redundant constraints are only valid because the way the first line is preset
"""

# 8-4-5 to 8-4-11
# 4 4 5 to 9 9 10
#  7-4-9
