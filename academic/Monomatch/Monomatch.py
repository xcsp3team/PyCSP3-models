"""
Construction of a mono-matching game.

This type of game is most well-known as Dobble or Spot-It, and contains a set of cards with symbols on them.
Each pair of cards share a single symbol.

The model, below, is close to (can be seen as the close translation of) the one submitted to the M2021 inizinc challenge.
However, the original model involved set variables.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, with a MIT Licence.

## Data
  Two integers (n,p)

## Model
  There are two variants:
    - a main one with the constraint NValues,
    - a '01" variant with auxiliary variables

  Constraints: Count, Lex, NValues, Sum

## Execution
  python Monomatch.py -data=[number,number]

## Links
  - https://en.wikipedia.org/wiki/Dobble
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
"""

from pycsp3 import *
import math

n, percentage = data

nSymbols = n * n + n + 1
nCards = math.floor((nSymbols * percentage) / 100)

# x[i,j] is the jth symbol on the ith card
x = VarArray(size=[nCards, n], dom=range(nSymbols))

satisfy(
    [Increasing(x[i], strict=True) for i in range(nCards)],

    LexIncreasing(x, strict=True)
)

if not variant():
    satisfy(
        NumberDistinctValues(
            within=x[i] + x[j]
        ) == 2 * n - 1 for i, j in combinations(nCards, 2)
    )


elif variant("01"):
    b = VarArray(size=[nCards, nSymbols], dom={0, 1})

    satisfy(
        [
            b[i][j] == ExactlyOne(x[i], value=j) for i in range(nCards) for j in range(nSymbols)
        ],

        [
            Sum(
                both(
                    b[i][k] == 1,
                    b[i][k] == b[j][k]
                ) for k in range(nSymbols)
            ) == 1 for i, j in combinations(nCards, 2)
        ]
    )

"""
1) the model with NValues is not very efficient (at least, with ACE) 
2) data used in 2021 are: (3,97) (4,75) (4,97) (5,50) (6,50)
3) DistinctValues is an alias for NVAlues
"""
