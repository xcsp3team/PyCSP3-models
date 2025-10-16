"""
The blocked n-queens problem is a variant of n-queens which has been proven to be NP-complete as a decision problem and #P-complete as a counting problem.
The input contains a list of squares which are blocked.
A solution to the problem is a solution to the n-queens problem containing no queen on any of the blocked squares.

See problem 080 at CSPLib.

## Data Example
  28-1449787798.json

## Model
  constraints: AllDifferent

## Execution
  python BlockedQueens.py -data=<datafile.json>
  python BlockedQueens.py -data=<datafile.txt> -parser=BlockedQueens_Parser.py

## Links
  - https://www.csplib.org/Problems/prob080/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, csplib, lpcp16, xcsp22
"""

from pycsp3 import *

n, blocks = data

# q[i] is the column where is put the ith queen (at row i)
q = VarArray(size=n, dom=range(n))

satisfy(
    # respecting blocks
    [q[i] != j for (i, j) in blocks],

    # no two queens on the same column
    AllDifferent(q),

    # no two queens on the same diagonal
    [abs(q[i] - q[j]) != abs(i - j) for i, j in combinations(n, 2)]
)

""" Comments
1) One could also additionally post (to make instances harder?):
  # controlling no two queens on the same upward diagonal
  AllDifferent(q[i] + i for i in range(n)),

  # controlling no two queens on the same downward diagonal
  AllDifferent(q[i] - i for i in range(n)),
"""
