"""

## Data Example
  example.json

## Model
  constraints: Cardinality, Sum

## Command Line
  python Bugs.py -data=<datafile.json>

## Tags
  recreational
"""

from pycsp3 import *

height, width = data.height, data.width
bugs, lengths = data.bugs, data.bugTypeLengths
nBugs, nTypes = len(bugs), len(lengths)
groups = [[i for i in range(nBugs) if data.bugs[i].type == k] for k in range(nTypes)]  # groups[k] is the group of bugs of type k

# x[i][j] is the index of a bug (or -1)
x = VarArray(size=[height, width], dom=range(-1, nBugs))

# n1[i] is the number of cells with value i
n1 = VarArray(size=nBugs, dom=range(height * width + 1))

# n2[i] is the number of cells with value i and a bug on it
n2 = VarArray(size=nBugs, dom=range(nBugs + 1))


def neighbors(i, j, k, l):
    return i == k and j in {l - 1, l + 1} or j == l and i in {k - 1, k + 1}


satisfy(
    # each bug cell can take either its bug index for value or the one of another bug of the same type
    [x[i][j] in groups[k] for (i, j, k) in bugs],

    # a bug cell value is smaller or equal to the bug index  tag(symmetry-breaking)
    [x[i][j] <= k for k, (i, j, _) in enumerate(bugs)],

    [n1[group[j]] <= (k - j) * lengths[i] for i, group in enumerate(groups) if (k := len(group),) for j in range(k)],

    # computing values of n1
    Cardinality(
        within=x,
        occurrences=n1
    ),

    # computing values of n2
    Cardinality(
        within=[x[i][j] for (i, j, _) in bugs],
        occurrences=n2
    ),

    # linking variables of n1 and n2
    [n2[i] * lengths[bugs[i].type] == n1[i] for i in range(nBugs)],

    # if two cells have the same value, then all cells in the rectangle they delimit must take this value
    [
        If(
            x[i][j] == x[k][l],
            Then=x[i][j] == x[m][n]
        ) for (i, j, k, l, m, n) in product(range(height), range(width), repeat=3)
        if i <= m <= k and not neighbors(i, j, k, l) and (i != k or j < l) and min(j, l) <= n <= max(j, l) and (m, n) != (i, j) and (m, n) != (k, l)
    ]
)

maximize(
    # maximizing the number of times a bug is in a rectangle whose index is different from the one of the bug
    Sum(n2[i] == 0 for i in range(nBugs))
)
