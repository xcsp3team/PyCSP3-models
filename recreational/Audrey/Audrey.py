"""
Problem proposed by Audrey at n-Side (see problem in OscaR).

Based on a little game I used to play in high school when I was getting bored in the classroom...
Draw a ten cells by ten cells board.
The purpose is to fill in all cells with numbers from 0 to 99.
You start by writing 0 in whatever cell.
From there on, you need to write the 1 by moving around in one of the following ways:
  - Move by 3 cells horizontally or vertically
  - Or move by 2 cells diagonally
Then, starting from the 1, you need to write the 2 using the same permitted moves, and so on.

The problem can be generalized for any order n.

## Data
  An integer n, the order of the board

## Model
  constraints: Circuit

## Execution
  python Audrey.py -data=number
  python Audrey.py -data=number -variant=display1
  python Audrey.py -data=number -variant=display2

## Tags
  academic, recreational
"""

from pycsp3 import *

n = data or 10
n2 = n * n


def domain_x(k):
    i, j = k // n, k % n
    possible_cells = [(i - 3, j), (i + 3, j), (i, j - 3), (i, j + 3), (i - 2, j - 2), (i - 2, j + 2), (i + 2, j - 2), (i + 2, j + 2)]
    return {p * n + q for p, q in possible_cells if 0 <= p < n and 0 <= q < n}


# x[i] is the index of the cell of the board following the ith cell in the circuit
x = VarArray(size=n2, dom=domain_x)

satisfy(
    # ensuring that we build a circuit
    Circuit(x)
)

if variant("display1"):
    # y[i] is the value put in the ith cell of the board
    y = VarArray(size=n2, dom=range(n2))

    satisfy(
        # linking values of the board
        [y[x[k]] == (y[k] + 1) % n2 for k in range(n2)],

        # putting 0 in the first cell  tag(symmetry-breaking)
        y[0] == 0
    )

elif variant("display2"):
    # b[i][j] is the value put in the cell at row i and column j of the board
    b = VarArray(size=[n, n], dom=range(n2))

    satisfy(
        # linking values of the board
        [b[x[k] // n][x[k] % n] == (b[k // n][k % n] + 1) % n2 for k in range(n2)],

        # putting 0 in the first cell  tag(symmetry-breaking)
        b[0][0] == 0
    )

""" Comments
1) The main model variant is sufficient to compute solutions.
   It is the fastest model. Hence, in a complex-world application, 
   adding constraints for pure presentational issue should be carefully thought.    
2) The variant 'display1' allows us to display the values (and not only the chaining).
   From this variant, to really get a matrix being printed, on can add:
     b = VarArray(size=[n, n], dom=range(n2))
     satisfy(
       b[k // n][k % n] == y[k] for k in range(n2)
     )     
3) The variant 'display2' allows us to directly print the values in a matrix.
   This involves a constraint 'ElementMatrix' whose computed value must be equal to a variable.    
4) We obtain 96 solutions for n=5 with the three variants.
"""
