"""
This is [Problem 032](https://www.csplib.org/Problems/prob032/) at CSPLib:

This problem arises from the Game of Life, invented by John Horton Conway in the 1960s and popularized by Martin Gardner in his Scientific American columns.
Life is played on a squared board, considered to extend to infinity in all directions. Each square of the board is a cell,
which at any time during the game is either alive or dead. A cell has eight neighbours.
The configuration of live and dead cells at time t leads to a new configuration at time t+1 according to the rules of the game:
 - if a cell has exactly three living neighbours at time t, it is alive at time t+1
 - if a cell has exactly two living neighbours at time t it is in the same state at time t+1 as it was at time t
 - otherwise, the cell is dead at time t+1

## Example
  Here is a solution for a 3x3 still-life with 6 live cells (the optimum). (source from CSPlib):
  ![Life3](https://www.csplib.org/Problems/prob032/assets/life3.jpg)

## Data
  A pair (n,m), where n is the number of rows and m the number of columns.

## Model
  There are two variants, a classical one and a "wastage" one.

  constraints: Sum, Table

## Execution
  python StillLife.py -data=[number,number]
  python StillLife.py -data=[number,number] -variant=wastage

## Links
  - https://www.csplib.org/Problems/prob032/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop


## Tags
  academic, csplib, xcsp24
"""

from pycsp3 import *

n, m = data or (8, 8)

if not variant():
    T = {(v, 0) for v in range(9) if v != 3} | {(2, 1), (3, 1)}

    # x[i][j] is 1 iff the cell at row i and col j is alive
    x = VarArray(size=[n, m], dom={0, 1})

    # a[i][j] is the number of alive neighbours
    a = VarArray(size=[n, m], dom=range(9))

    satisfy(
        # computing the numbers of alive neighbours
        [Sum(x.around(i, j)) == a[i][j] for i in range(n) for j in range(m)],

        # imposing rules of the game
        [(a[i][j], x[i][j]) in T for i in range(n) for j in range(m)],

        # imposing rules for ensuring valid dead cells around the board
        [
            [x[0][i:i + 3] != (1, 1, 1) for i in range(m - 2)],
            [x[-1][i: i + 3] != (1, 1, 1) for i in range(m - 2)],
            [x[i:i + 3, 0] != (1, 1, 1) for i in range(n - 2)],
            [x[i:i + 3, - 1] != (1, 1, 1) for i in range(n - 2)]
        ],

        # tag(symmetry-breaking)
        (
            x[0][0] >= x[n - 1][n - 1],
            x[0][n - 1] >= x[n - 1][0]
        ) if n == m else None
    )

    maximize(
        # maximizing the number of alive cells
        Sum(x)
    )

elif variant("wastage"):
    assert n == m


    def condition_for_tuple(t0, t1, t2, t3, t4, t5, t6, t7, t8, wa):
        s3 = t1 + t3 + t5 + t7
        s1 = t0 + t2 + t6 + t8 + s3
        s2 = t0 * t2 + t2 * t8 + t8 * t6 + t6 * t0 + s3
        return (t4 != 1 or (2 <= s1 <= 3 and (s2 > 0 or wa >= 2) and (s2 > 1 or wa >= 1))) and \
            (t4 != 0 or (s1 != 3 and (0 < s3 < 4 or wa >= 2)) and (s3 > 1 or wa >= 1))


    T = {(*t, i) for t in product(range(2), repeat=9) for i in range(3) if condition_for_tuple(*t, i)}

    # x[i][j] is 1 iff the cell at row i and col j is alive (note that there is a border)
    x = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, n + 1} else {0, 1})

    # w[i][j] is the wastage for the cell at row i and col j
    w = VarArray(size=[n + 2, n + 2], dom={0, 1, 2})

    # ws[i] is the wastage sum for cells at row i
    ws = VarArray(size=n + 2, dom=range(2 * (n + 2) * (n + 2) + 1))

    satisfy(
        # ensuring that cells at the border remain dead
        [
            [x[1][j:j + 3] != (1, 1, 1) for j in range(n)],
            [x[n][j:j + 3] != (1, 1, 1) for j in range(n)],
            [x[i:i + 3, 1] != (1, 1, 1) for i in range(n)],
            [x[i:i + 3, n] != (1, 1, 1) for i in range(n)]
        ],

        # still life + wastage constraints
        [(x[i - 1:i + 2, j - 1:j + 2], w[i][j]) in T for i in range(1, n + 1) for j in range(1, n + 1)],

        # managing wastage on the border
        [
            [(w[0][j] + x[1][j] == 1, w[n + 1][j] + x[n][j] == 1) for j in range(1, n + 1)],
            [(w[i][0] + x[i][1] == 1, w[i][n + 1] + x[i][n] == 1) for i in range(1, n + 1)]
        ],

        # summing wastage
        [Sum(w[0] if i == 0 else [ws[i - 1], w[i]]) == ws[i] for i in range(n + 2)],

        # tag(redundant)
        [ws[n + 1] - ws[i] >= 2 * ((n - i) // 3) + n // 3 for i in range(n + 1)]
    )

    maximize(
        # maximizing the number of alive cells
        (2 * n * n + 4 * n - ws[-1]) // 4
    )

""" Comments
1) We could have posted unary constraints instead of identifying specific cells
   at the border assumed to be dead, when creating arrays of variables, like:
 [
   [(x[0][j] == 0, x[-1][j] == 0) for j in range(n + 2)],
   [(x[i][0] == 0, x[i][-1] == 0) for i in range(n + 2)],
 ],

2) In order to generate automatically slide constraints when handling rules for the boarder, we could
   post groups of constraints separately, i.e., write:

 # imposing rules for ensuring valid dead cells around the board
 [x[0][i:i + 3] != (1, 1, 1) for i in range(m - 2)],
 ... (while using the option -recognizeSlides)

3) We could use extension constraints instead of intension constraints, which would give:
  [x[0][i:i + 3] not in {(1, 1, 1)} for i in range(m - 2)],
  By the way, note that expressing such intension constraints are possible here because x[0][i:i + 3] has type 'ListVar'
  If it was not the case, as for example in: (x[0][0], x[0][1], x[0][2]) != (1,1,1), we would have to call cp_array
  which would give : cp_array(x[0][0], x[0][1], x[0][2]) != (1,1,1)
  
4) Data used for the 2024 Competition: [(5,5), (8,8), (8,10), (9,9), (9,12), (10,10), (10,14),(12,12), (12,18)]
                    variant "wastage": [(5,5), (10,10), (15,15), (20,20), (30,30), (40,40), (50,50)]
"""
