"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  An integer n

## Model
  constraints: Count, Lex, Sum

## Execution
  python MQueens.py -data=[number]

## Links
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  academic, mzn14
"""

from pycsp3 import *

n = data or 11

N = range(n)

perms = [[i * n + j if k == 0 else (n - j - 1) * n + i if k == 1 else (n - i - 1) * n + (n - j - 1) if k == 2 else i * n + (n - j - 1) for i in N for j in N]
         for k in range(4)]


def scope(i, j, k):
    return [x[p][q] for p, q in [(i + k, j + k), (i - k, j + k), (i + k, j - k), (i - k, j - k)] if 0 <= p < n and 0 <= q < n]


# x[i][j] is 1 if a queen is present in the cell with coordinates (i,j)
x = VarArray(size=[n, n], dom={0, 1})

# q[i] is the position (or 0) of the queen on the ith row
q = VarArray(size=n, dom=range(n + 1))

flat_x = flatten(x)

satisfy(
    # constraining the presence of queens
    [
        x[i][j] == conjunction(
            NotExist(x[i][k] for k in N if k != j),
            NotExist(x[k][j] for k in N if k != i),
            NotExist(scope(i, j, k) for k in N[1:])
        ) for i in N for j in N
    ],

    # computing the position of queens in rows
    [q[i] == Sum((j + 1) * x[i][j] for j in N) for i in N],

    # tag(symmetry-breaking)
    [LexIncreasing(flat_x, [flat_x[pj[pi.index(k)]] for k in range(n * n)]) for i, pi in enumerate(perms) for j, pj in enumerate(perms) if i != j]
)

minimize(
    # minimizing the number of queens
    Sum(q[i] > 0 for i in N)
)

""" Comments
1) For symmetry-breaking, i != j should be i < j ?
2) Data used in 2014 are: 11, 12, 13, 20, 31
3) It is also possible to write:
  [x[i][j] == NotExist(x[i][k] for k in range(n) if k != j) & NotExist(x[k][j] for k in range(n) if k != i)
  & NotExist(disjunction(scope(i, j, k)) for k in range(1, n) if len(scope(i, j, k)) > 0) for i in range(n) for j in range(n)],
"""
