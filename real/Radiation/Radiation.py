"""
The problem of decomposing an integer matrix into a weighted sum of binary matrices has received much attention in recent years,
largely due to its application in radiation treatment for cancer.
See paper whose reference is given below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Sebastian Brand.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01.json

## Model
  constraints: Sum

## Execution
  python Radiation.py -data=<datafile.json>
  python Radiation.py -data=<datafile.dzn> -parser=Radiation_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-010-9104-1
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  real, mzn08, mzn12, mzn13, mzn15, mzn20
"""

from pycsp3 import *

intensity = data  # intensity matrix
n, m = len(intensity), len(intensity[0])
nIntensities = max(v for t in intensity for v in t) + 1  # +1 because we also have 0
sumIntensities = sum(sum(t) for t in intensity)
nCells = n * m + 1  # +1 to avoid systematically adding 1 in the model

B = range(1, nIntensities)

# z1 is the total beam-on time
z1 = Var(dom=range(sumIntensities + 1))

# z2 is the number of shape matrices
z2 = Var(dom=range(nCells))

# x[b] is the number of shape matrices with associated beam-on time b
x = VarArray(size=nIntensities, dom=lambda b: range(nCells) if b > 0 else {0})

# q[i][j][b] is the number of shape matrices having associated beam-on time b and exposing cell (i,j)
q = VarArray(size=[n, m, nIntensities], dom=lambda i, j, b: range(nCells) if b > 0 else {0})

satisfy(
    # computing z1
    z1 == Sum(b * x[b] for b in B),

    # computing z2
    z2 == Sum(x),

    # respecting the specified intensity in each cell
    [Sum(b * q[i][j][b] for b in B) == intensity[i][j] for i in range(n) for j in range(m)],

    # setting upper bounds on increments
    [x[b] >= q[i][0][b] + Sum(max(q[i][j][b] - q[i][j - 1][b], 0) for j in range(1, m)) for i in range(n) for b in B]
)

minimize(
    # minimizing (beam-time,number of shapes)
    nCells * z1 + z2
)
