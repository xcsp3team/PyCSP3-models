"""
Given four integers n, m, d and k, the goal is to find n vectors of size m where each value lies between 0 and d (exclusive),
and every two vectors have a Hamming distance at most equal to k

## Data
  four integers n, m, d, and k

## Model
  constraints: Count, Lex

## Execution
  python Hamming.py -data=[number,number,number,number]
  python Hamming.py -data=[number,number,number,number] -variant=mini

## Links
  - https://en.wikipedia.org/wiki/Hamming_distance
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
"""

from pycsp3 import *

n, m, d, k = data or (9, 4, 3, 3)

# x[i][j] is the jth value of the ith vector
x = VarArray(size=[n, m], dom=range(d))

if not variant():

    satisfy(
        # ensuring a Hamming distance of at least 'k' between any two vectors
        [Hamming(row1, row2) >= k for row1, row2 in combinations(x, 2)],

        # tag(symmetry-breaking)
        LexIncreasing(x)
    )

elif variant("mini"):
    # TODO : using tables?
    satisfy(
        x[0][0] == (x[0][1] > x[0][2])  # TODO illustrtation: not in the perimeter of mini-tracks

    )

""" Comments
1) 72 solutions for n=9 (and no solution for n=10)

2) Data used for the 2024 competition: [(20,10,3,5), (20,10,3,6), (20,10,3,7), (20,10,3,8), (20,10,5,7), (20,10,5,8), (20,10,5,9),
(20,10,5,10), (30,15,7,12), (30,15,7,13), (30,15,7,14), (30,15,7,15)]
"""
