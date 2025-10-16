"""
A binary puzzle (also known as a binary Sudoku) is a puzzle played on an n × n grid;
initially some of the cells may contain 0 or 1 (but this is not the case for the 2023 competition).
One has to fill the remaining empty cells with either 0 or 1 according to the following rules:
  -  no more than two similar numbers next to or below each other are allowed,
  -  each row and each column should contain an equal number of zeros and ones,
  - each row is unique and each column is unique.

## Data
  A unique integer n

## Model
  constraints: AllDifferentList, Regular, Sum

## Execution
  python BinaryPuzzle.py -data=number
  python BinaryPuzzle.py -data=number -variant=regular

## Links
  - https://www.researchgate.net/publication/243972408_Binary_Puzzle_is_NP-complete
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

assert not variant() or variant("regular")

n = data or 20

assert n % 2 == 0
m = n // 2

# x[i][j] is the value in the cell of the grid at coordinates (i,j)
x = VarArray(size=[n, n], dom={0, 1})

if not variant():
    satisfy(
        # ensuring the same number of 0s and 1s in rows
        [Sum(x[i]) == m for i in range(n)],

        # ensuring the same number of 0s and 1s in columns
        [Sum(x[:, j]) == m for j in range(n)],

        # forbidding sequences of 3 consecutive 0s or 1s in rows
        [Sum(x[i, j:j + 3]) in range(1, 3) for i in range(n) for j in range(n - 2)],

        # forbidding sequences of 3 consecutive 0s or 1s in columns
        [Sum(x[i:i + 3, j]) in range(1, 3) for j in range(n) for i in range(n - 2)]
    )

elif variant("regular"):
    pairs = [(j, k) for j in range(3) for k in range(3) if (j == 0 and k > 0) or (j > 0 and k == 0)]

    q = Automaton.q
    t = [(q(0, 0, 0), 0, q(0, 1, 0)), (q(0, 0, 0), 1, (q(1, 0, 1)))] \
        + [(q(i, j, k), 0, q(i, j + 1, 0)) for i in range(m + 1) for j, k in pairs if j < 2] \
        + [(q(i, j, k), 1, q(i + 1, 0, k + 1)) for i in range(m) for j, k in pairs if k < 2]
    A = Automaton(start=q(0, 0, 0), final=[q(m, j, k) for j, k in pairs], transitions=t)

    satisfy(
        # ensuring the same number of 0s and 1s in rows, while forbidding sequences of 3 consecutive 0s or 1s
        [x[i] in A for i in range(n)],

        # ensuring the same number of 0s and 1s in columns, while forbidding sequences of 3 consecutive 0s or 1s
        [x[:, j] in A for j in range(n)]
    )

satisfy(
    # forbidding identical rows
    AllDifferentList(x[i] for i in range(n)),  # .to_table(),

    # forbidding identical columns
    AllDifferentList(x[:, j] for j in range(n))  # .to_table()
)

""" Comments
1) For XCSP competitions, before 2024, we needed to discard or translate in tables (calling .to_table())
   the AllDifferentList constraints
2) For finding a first solution, the regular model is far more efficient (at least with default heuristics)
  (a few seconds for n=50, 60 or 70)  
3) For being compatible with the competition mini-track, we use for the main variant:
   [Sum(x[i, j:j + 3]) >= 1 for i in range(n) for j in range(n - 2)],
   [Sum(x[i, j:j + 3]) <= 2 for i in range(n) for j in range(n - 2)],
4) We can write:
   [Sum(x[i, j:j + 3]) in {1,2} for i in range(n) for j in range(n - 2)], 
5) Data for the 2023 competition are: [20, 40, 60, 80, 100, 120]
"""
