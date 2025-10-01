"""
Put n pennies on a chessboard, so that all distances between pennies are distinct.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.
The original model involves an option type while we use the special value -1.

## Data
  An integer n

## Model
  constraints: AllDifferent, Sum

## Execution
  python Pennies.py -data=number

## Links
  - https://blog.computationalcomplexity.org/2023/06/can-you-put-n-pennies-on-n-x-n.html
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  academic, mzn23
"""

from pycsp3 import *

n = data or 5

# p[i] is 1 if the ith penny is placed
p = VarArray(size=n, dom={0, 1})

# x[i] is the x-coordinate of the ith penny if placed, or -1
x = VarArray(size=n, dom=range(-1, n))

# y[i] is the y-coordinate of the ith penny if placed, or -1
y = VarArray(size=n, dom=range(-1, n))

# xy[i] is the square index of the ith penny if placed, or -1
xy = VarArray(size=n, dom=range(-1, n * n))

# d[i][j] is the distances between the ith and jth pennies if placed, or -1
d = VarArray(size=[n, n], dom=lambda i, j: range(-1, (n - 1) * (n - 1) * 2 + 1) if i < j else None)

satisfy(
    # all pennies on different squares
    AllDifferent(xy, excepting=-1),

    # computing distances
    [
        d[i][j] == ift(
            both(p[i], p[j]),
            Then=(x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2,
            Else=-1
        ) for i, j in combinations(n, 2)
    ],

    # all distances are different
    AllDifferent(d, excepting=-1),

    # connecting position variables
    [
        xy[i] == ift(
            p[i],
            Then=x[i] * n + y[i],
            Else=-1
        ) for i in range(n)
    ],

    # ensuring coherence of position variables
    [
        (
            p[i] == (x[i] != -1),
            p[i] == (y[i] != -1),
            p[i] == (xy[i] != -1)
        ) for i in range(n)
    ],

    # tag(symmetry-breaking)
    [
        Decreasing(p),

        [
            If(
                p[i + 1],
                Then=xy[i] < xy[i + 1]
            ) for i in range(n - 1)
        ]
    ]
)

maximize(
    # maximizing the number of present pennies
    Sum(p)
)

""" Comments
1) For getting unsatisfiable instances for large values of n, remove -1 from the domain of distances
2) The opt variables of MZN are handled by using the special value -1 
3) Data used in 2023 are : [5, 7, 8, 9, 12]
"""
