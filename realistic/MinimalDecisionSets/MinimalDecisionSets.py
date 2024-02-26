"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  breast-cancer-train4.json

## Model
  constraints: Count, Sum

## Execution
  python MinimalDecisionSets.py -data=<datafile.json>
  python MinimalDecisionSets.py -data=<datafile.dzn> -parser=MinimalDecisionSets_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

nItems, db = data
n = 5  # max number of nodes

nFeatures = len(db[0])
target, dummy = nFeatures - 1, nFeatures  # dummy is a special value

for row in db:
    row.append(0)  # adding 0 for the dummy value (simpler for the element constraint later)

# sgn[j] is 1 if the corresponding feature is true
sgn = VarArray(size=n, dom={0, 1})

# ftr[j] is the feature discriminating at the jth node (or dummy if unused)
ftr = VarArray(size=n, dom=range(nFeatures + 1))

# vld[j,i] is 1 if the ith item is valid at the jth node
vld = VarArray(size=[n, nItems], dom={0, 1})

# mis[i] is 1 if the ith item is misclassified
mis = VarArray(size=nItems, dom={0, 1})

# unused[j] is 1 when the jth node is  not used
unused = VarArray(size=n, dom={0, 1})

# leaf[j] is 1 if the j-1th node is a leaf
leaf = VarArray(size=n + 1, dom=lambda i: {0, 1} if i > 0 else {1})

# z is the number of used nodes
z = Var(dom=range(n + 1))

satisfy(
    # we have a leaf when reaching the target
    [leaf[j + 1] == (ftr[j] == target) for j in range(n)],

    # unused nodes correspond to the dummy feature
    [unused[j] == (ftr[j] == dummy) for j in range(n)],

    # computing z
    Sum(unused) == n - z,

    # constraining leaf and unused nodes
    (
        leaf[1] == 0,
        either(leaf[-1], unused[- 1]),
        [If(unused[i], Then=either(unused[i - 1], leaf[i])) for i in range(1, n)],
        [If(unused[i], Then=unused[i + 1]) for i in range(n - 1)],
        [If(z < i + 1, Then=unused[i]) for i in range(n)],
        [If(unused[i], Then=sgn[i] == 0) for i in range(n)]
    ),

    # validity propagation
    (
        [vld[0][i] == 1 for i in range(nItems)],
        [
            vld[j + 1][i] == either(
                leaf[j + 1],
                both(vld[j][i], db[i][ftr[j]] == sgn[j])
            ) for j in range(n - 1) for i in range(nItems)
        ],
    ),

    # correctness of leaves
    [
        If(
            leaf[j + 1], vld[j][i],
            Then=either(
                db[i][-2] == sgn[j],
                mis[i]
            )
        ) for i in range(nItems) for j in range(n)
    ],

    # every item must be covered by one leaf (or is misclassified)
    [
        either(
            mis[i],
            Exist(both(leaf[j + 1], vld[j][i]) for j in range(n))
        ) for i in range(nItems)
    ]
)

minimize(
    # minimizing the number of misclassified items, combined with the number of used nodes
    Sum(mis) + (nItems // 20) * z
)

"""
1) note that we have added a column (with 0) to db to simplify some element constraints
"""
