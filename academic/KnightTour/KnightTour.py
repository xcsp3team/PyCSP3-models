"""
A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once.
If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately,
following the same path), the tour is closed; otherwise, it is open.

## Data
  A number n, the size of the board.

## Example
  This is an animation on a 5x5 board (source: [wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour))
  ![knight tour](https://upload.wikimedia.org/wikipedia/commons/c/ca/Knights-Tour-Animation.gif)

## Model
  There are two variant, a main one with intensional constraints, and one with table constraints

  constraints: AllDifferent, Table

## Execution
  python KnightTour.py -data=number
  python KnightTour.py -data=number -variant=table-2
  python KnightTour.py -data=number -variant=table-3

## Links
  - https://en.wikipedia.org/wiki/Knight%27s_tour

## Tags
  academic
"""

from pycsp3 import *

n = data or 8

# x[i] is the cell number where the ith knight is put
x = VarArray(size=n * n, dom=range(n * n))

satisfy(
    # knights are put in different cells
    AllDifferent(x),

    # putting the first knight in the first cell, and the second knight in the first possible cell  tag(symmetry-breaking)
    [
        x[0] == 0,
        x[1] == n + 2
    ]
)

if not variant():
    pairs = [(i, (i + 1) % (n * n)) for i in range(n * n)]

    satisfy(
        # two successive knights are at a knight jump apart
        (d1 == 1) & (d2 == 2) | (d1 == 2) & (d2 == 1) for i, j in pairs if (d1 := abs(x[i] // n - x[j] // n), d2 := abs(x[i] % n - x[j] % n))
    )

elif variant("table"):
    r = int(subvariant())
    assert r > 1 and n % (r - 1) == 0


    def jump(i, j):
        t = []
        if i - 2 >= 0:
            if j - 1 >= 0:
                t.append((i - 2) * n + j - 1)
            if j + 1 < n:
                t.append((i - 2) * n + j + 1)
        if i + 2 < n:
            if j - 1 >= 0:
                t.append((i + 2) * n + j - 1)
            if j + 1 < n:
                t.append((i + 2) * n + j + 1)
        if j - 2 >= 0:
            if i - 1 >= 0:
                t.append((i - 1) * n + j - 2)
            if i + 1 < n:
                t.append((i + 1) * n + j - 2)
        if j + 2 < n:
            if i - 1 >= 0:
                t.append((i - 1) * n + j + 2)
            if i + 1 < n:
                t.append((i + 1) * n + j + 2)
        return sorted(t)


    jumps = [jump(i, j) for i in range(n) for j in range(n)]


    def table_recursive(i, tmp):
        if i == len(tmp):
            T.append(tuple(tmp[:]))
        else:
            for v in jumps[tmp[i - 1]]:
                if len([j for j in range(0, i - 1) if tmp[j] == v]) == 0:
                    tmp[i] = v
                    table_recursive(i + 1, tmp)


    T = list()
    for i in range(n * n):
        table_recursive(1, [i] + [0] * (r - 1))

    satisfy(
        # two successive knights are at a knight jump apart
        x[i:i + r] in T for i in range(0, n * n, r - 1)
    )

""" Comments
1) it is possible to use extension constraints instead of intension constraints (see, e.g., the problem QueensKnights)
2) it is faster to use a list than a set for the table T
3) Note that (notably, by index auto-adjustment):
 x[i:i + r]
  is equivalent to:
 (x[(i + j) % (n * n)] for j in range(r))   

"""
