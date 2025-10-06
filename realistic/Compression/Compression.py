"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  bin-07.json

## Model
  constraints: Cardinality, Element, Sum

## Execution
  python Compression.py -data=<datafile.json>
  python Compression.py -data=<datafile.json> -variant=mzn

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
"""

from pycsp3 import *
from pycsp3.dashboard import options

#  option set to avoid writing  [((aux := Var()) == sx[cp[i]] + ci[i], text[aux] == text[i]) for i in range(n)]
#  instead of [text[sx[cp[i]] + ci[i]] == text[i] for i in range(n)]
options.force_element_index = True

assert not variant() or variant("mzn")

nPatterns, maxPatternLength, text = data

n = len(text)
nNodes = 2 * nPatterns - 1
root, nInternals = 0, nPatterns - 1  # maximal number of internal nodes (not leaves)

# sx[j] is the position of the first letter of the jth slice/pattern (if used)
sx = VarArray(size=nPatterns, dom=range(n))

# sl[j] is the length of the jth slice/pattern (if used)
sl = VarArray(size=nPatterns, dom=range(maxPatternLength + 1))

# cp[i] is the pattern used for th ith letter
cp = VarArray(size=n, dom=range(nPatterns))

# ci[i] is the index in the used pattern of the ith letter
ci = VarArray(size=n, dom=range(maxPatternLength))

# parent[k] is the parent of the kth node (or -1)
parent = VarArray(size=nNodes, dom=range(-1, nInternals))

# pcount[k] is the number of times the kth node is a parent
pcount = VarArray(size=nInternals, dom={0, 2})

# costs[k] is the cost of the kth node computed from the cost of its parent
costs = VarArray(size=nNodes, dom=range(nPatterns + 1))

# uses[j] is the number of times the jth pattern is used
uses = VarArray(size=nPatterns, dom=range(n + 1))

satisfy(
    # ensuring that the covered byte matches the pattern that covers it
    [
        text[sx[cp[i]] + ci[i]] == text[i]
        for i in range(n)
    ],

    # ensuring that cover indexes follow in sequence (until the end of a pattern)
    [
        ci[0] == 0,
        [
            If(
                ci[i - 1] + 1 == sl[cp[i - 1]],
                Then=ci[i] == 0,
                Else=[cp[i] == cp[i - 1], ci[i] == ci[i - 1] + 1]
            ) for i in range(1, n)
        ],
        ci[-1] + 1 == sl[cp[-1]]
    ],

    # managing parents
    [
        parent[root] == -1,
        [
            (parent[nInternals + j] != -1) == (sl[j] > 0)
            for j in range(nPatterns)
        ],
        Cardinality(
            within=parent,
            occurrences={k: pcount[k] for k in range(nInternals)}
        )
    ],

    # computing costs
    [
        costs[root] == 0,
        [
            If(
                parent[k] != -1,
                Then=costs[k] == costs[parent[k]] + 1,
                Else=costs[k] == 0
            ) for k in range(1, nNodes)
        ]
    ],

    # computing uses
    [
        uses[j] == Sum(
            both(
                cp[i] == j,
                ci[i] == 0
            ) for i in range(n)
        ) for j in range(nPatterns)
    ]
)

if variant("mzn"):
    used_nodes = Var(dom=range(nInternals + 1))  # % Nodes after this are unused

    satisfy(
        parent[k] <= used_nodes for k in range(nNodes)
    )

minimize(
    # minimizing the size of the encoding
    Sum(sl[j] * 8 + costs[nInternals + j] * (uses[j] + 1) for j in range(nPatterns))
)

""" Comments
1) The variant "mzn" includes stuff from the original model, that seems useless (except maybe for guiding search)
2) It seems that this model (actually, the original one) can be optimized/improved
"""
