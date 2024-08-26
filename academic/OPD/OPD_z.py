"""
An OPD (v,b,r) problem is to find a binary matrix of v rows and b columns such that:
   - each row sums to r,
   - the dot product between any pair of distinct rows is minimal

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2017 Minizinc challenges.
The MZN model was proposed by Pierre Flener and Jean-Noel Monette (loosely based on Ralph Becket's BIBD model)
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  Three integers (v,b,r)

## Model
  constraints: Lex, Sum

## Execution
  python OPD_z.py -data=[number,number,number]

## Links
  - https://www.csplib.org/Problems/prob065/
  - https://link.springer.com/article/10.1007/s10601-006-9014-4
  - https://www.sciencedirect.com/science/article/abs/pii/S1571065314000596?via%3Dihub
  - https://link.springer.com/chapter/10.1007/11564751_7
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  academic, csplib, mzn15, mzn17
"""

from pycsp3 import *

v, b, r = data


def lower_bound():
    rv = r * v
    ceil_rv = rv // b + (1 if rv % b != 0 else 0)
    num = (ceil_rv * ceil_rv * (rv % b) + (rv // b) * (rv // b) * (b - (rv % b)) - rv)
    den = v * (v - 1)
    return num // den + (1 if num % den != 0 else 0)


# x[i][j] is the value in the cell at coordinates (i,j)
x = VarArray(size=[v, b], dom={0, 1})

# z is the value of lambda
z = Var(dom=range(lower_bound(), b + 1))

satisfy(
    # every row must sum to r
    [Sum(x[i]) == r for i in range(v)],

    # the dot product of every pair of distinct rows must be at most equal to lambda
    [x[i] * x[j] <= z for i, j in combinations(v, 2)],

    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)

minimize(
    # minimizing the value of lambda
    z
)

""" Comments
1) Data used in challenges are:
  for 2015: (10,350,100) (10,100,30) (10,30,9) (11,22,10) (13,26,6)
  for 2017: (15,350,100) (13,250,80) (6,50,25) (6,60,30) (8,28,14)
"""
