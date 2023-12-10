"""
This naive model for the magic sequence allows us to test the ability of solvers to handle many simple constraints at the same time.
For a problem of size 50, roughly 5000 propagators are needed.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008/2013/2015 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  An integer n

## Model
  constraints: Sum

## Execution
  python NaiveMagicSequence.py -data=<number>

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  academic, mzn08, mzn13, mzn15
"""

from pycsp3 import *

n = data

# x[i] is the ith value of the sequence
x = VarArray(size=n, dom=range(n))

satisfy(
    # each value i occurs exactly x[i] times in the sequence
    Sum(x[j] == i for j in range(n)) == x[i] for i in range(n)
)

"""
1) data used in challenges are:
  20, 40, 60, 80, 100, 150, 200, 300, 400, 500 for 2008
  99, 143, 202, 395, 478 for 2013
  83, 176, 207, 269, 396 for 2015
"""
