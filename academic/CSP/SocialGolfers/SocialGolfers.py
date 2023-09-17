"""
This is the [problem 010](https://www.csplib.org/Problems/prob010/) of the CSPLib.

"*The coordinator of a local golf club has come to you with the following problem. In their club, there are 32 social golfers, e
ach of whom play golf once a week, and always in groups of 4. They would like you to come up with a schedule of play for these golfers,
to last as many weeks as possible, such that no golfer plays in the same group as any other golfer on more than one occasion.
The problem can easily be generalized to that of scheduling groups of golfers over at most weeks, such
that no golfer plays in the same group as any other golfer twice (i.e. maximum socialisation is achieved).
For the original problem, the values of and are respectively 8 and 4.*".

## Data
A triplet \[n,s,w], n is the number of groups, s the size of the groups and w the number of weeks.

## Model(s)
You can  find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/SocialGolfers/).

There are 2 variants of this problem one with constraints sum the other with constraints in intension.

constraints: Cardinality, Intension, Sum, LexIncreasing

## Command Line
python SocialGolfers.py
python SocialGolfers.py -data=[5,3,6]
python SocialGolfers.py -data=[5,3,6] -variant=1

## Tags
 academic notebook
"""

from pycsp3 import *

nGroups, size, nWeeks = data or (4, 4, 5)  # size is the size of the groups
nPlayers = nGroups * size

if not variant():
    # g[w][p] is the group admitting on week w the player p
    g = VarArray(size=[nWeeks, nPlayers], dom=range(nGroups))

    satisfy(
        # ensuring that two players don't meet more than one time
        [(g[w1][p1] != g[w1][p2]) | (g[w2][p1] != g[w2][p2]) for w1, w2 in combinations(nWeeks, 2) for p1, p2 in combinations(nPlayers, 2)],

        # respecting the size of the groups
        [Cardinality(g[w], occurrences={i: size for i in range(nGroups)}) for w in range(nWeeks)],

        # tag(symmetry-breaking)
        [
            LexIncreasing(g, matrix=True),

            [g[0][p] == p // size for p in range(nPlayers)],

            [g[w][k] == k for k in range(size) for w in range(1, nWeeks)]
        ]
    )
elif variant("01"):
    # x[w][g][p] is 1 iff on week w the group g admits the player p
    x = VarArray(size=[nWeeks, nGroups, nPlayers], dom={0, 1})

    # tw[p1][p2][w] is 1 iff players p1 and p2 play together on week w
    tw = VarArray(size=[nPlayers, nPlayers, nWeeks], dom=lambda p1, p2, w: {0, 1} if p1 < p2 else None)

    # twg[p1][p2][w][g] is 1 iff players p1 and p2 play together on week w in group g
    twg = VarArray(size=[nPlayers, nPlayers, nWeeks, nGroups], dom=lambda p1, p2, w, g: {0, 1} if p1 < p2 else None)

    satisfy(
        # each week, each player plays exactly once
        [Sum(x[w][g][p] for g in range(nGroups)) == 1 for w in range(nWeeks) for p in range(nPlayers)],

        # each week, each group contains exactly the right number of players
        [Sum(x[w][g]) == size for w in range(nWeeks) for g in range(nGroups)],

        # two players cannot meet twice
        [Sum(tw[p1][p2]) <= 1 for p1, p2 in combinations(nPlayers, 2)],

        # deciding when two players play together
        [Sum(twg[p1][p2][w]) == tw[p1][p2][w] for p1, p2 in combinations(nPlayers, 2) for w in range(nWeeks)],

        # deciding when two players play in the same group
        [x[w][g][p1] * x[w][g][p2] == twg[p1][p2][w][g] for w in range(nWeeks) for g in range(nGroups) for p1, p2 in combinations(nPlayers, 2)],

        # tag(symmetry-breaking)
        [
            # each week, groups are strictly ordered
            [LexDecreasing(x[w], strict=True) for w in range(nWeeks)],

            # weeks are strictly ordered (it suffices to consider the first group)
            LexDecreasing([x[w][0] for w in range(nWeeks)], strict=True),

            # golfers are strictly ordered
            LexDecreasing([[x[w][g][p] for w in range(nWeeks) for g in range(nGroups)] for p in range(nPlayers)], strict=True)
        ]
    )
