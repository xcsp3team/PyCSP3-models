"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011/2015 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  Two integers n and m

## Execution
  python GridColoring.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  academic, mzn10, mzn11, mzn15
"""

from pycsp3 import *

n, m = data

# x[i][j] is the color for the cell with coordinates (i,j)
x = VarArray(size=[n, m], dom=range(1, min(n, m) + 1))

# z is the number of used colors
z = Var(dom=range(1, min(n, m) + 1))

satisfy(
    # constraining the objective
    [x[i][j] <= z for i in range(n) for j in range(m)],

    # coloring rules
    [
        disjunction(
            x[i][k] != x[i][l],
            x[i][l] != x[j][l],
            x[j][k] != x[j][l],
            x[i][k] != x[j][k]
        ) for i, j in combinations(n, 2) for k, l in combinations(m, 2)
    ]
)

minimize(
    z
)

"""
1) data used in challenges are:
  (5,6) (7,8) (10,10) (12,13) (15,16) in 2010 and 2011
  (4,8) (4,11) (10,5) (13,11) (19,17) in 2015
"""
