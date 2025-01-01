"""
There are n countries.
Each pair of two countries is either at war or has a peace treaty.
Each pair of two countries that has a common enemy has a peace treaty.
What is the minimum number of peace treaties?

The minimum number of peace treaties for n in [2..12] seems to be floor(n^2/4), see https://oeis.org/A002620
Hence, it is 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81, ...

## Data
  an integer n

## Model
  constraints: Sum

## Execution
  python WarOrPeace.py -data=number
  python WarOrPeace.py -data=number -variant=or

## Links
  - https://oeis.org/A002620
  - http://www.hakank.org/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  academic, xcsp22
"""

from pycsp3 import *

n = data or 8
WAR, PEACE = 0, 1

# x[i][j] is 1 iff countries i and j have a peace treaty
x = VarArray(size=[n, n], dom=lambda i, j: {WAR, PEACE} if i < j else None)

if not variant():
    satisfy(
        If(
            x[i][j] != PEACE,
            Then=NotExist(
                both(
                    x[min(i, k)][max(i, k)] == WAR,
                    x[min(j, k)][max(j, k)] == WAR
                ) for k in range(n) if different_values(i, j, k)
            )
        ) for i, j in combinations(n, 2)
    )

elif variant("or"):
    satisfy(
        If(
            x[i][j] != PEACE,
            Then=[
                # x[i][j] == WAR,  # was present when generating instances of the 2022 competition, but totally useless
                conjunction(
                    either(
                        x[k][i] == PEACE,
                        x[k][j] == PEACE
                    ) for k in range(i)
                )
            ]
        ) for i, j in combinations(range(1, n), 2)
    )

minimize(
    # minimizing the number of peace treaties
    Sum(x)
)

""" Comments
1) The model variant 'or' seems to be far more efficient
"""
