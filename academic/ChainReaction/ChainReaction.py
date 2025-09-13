"""
From JaneStreet:
    Write down a chain of integers between 1 and 100, with no repetition, such that if x and y are consecutive numbers in the chain,
    then x evenly divides y or y evenly divides x. Here is an example of such a chain, with length 12:
      37, 74, 2, 8, 4, 16, 48, 6, 3, 9, 27, 81
    What is the longest chain you can find?

## Data
  two numbers n and k

## Model
  constraints: AllDifferent, Sum

## Execution
  python ChainReaction.py -data=[number,number]
  python ChainReaction.py -data=[number,number] -variant=opt

## Links
  - https://www.janestreet.com/puzzles/chain-reaction-index/

## Tags
  academic, janestreet, xcsp25
"""

from pycsp3 import *

n, k = data or (20, 100)

# x[i] is the ith value of the chain
x = VarArray(size=n, dom=range(1, k + 1))

satisfy(
    # ensuring all values are different
    AllDifferent(x)
)

if variant("mini"):
    T = [(v, w) for v in range(1, k + 1) for w in range(1, k + 1) if v % w == 0 or w % v == 0]

    satisfy(
        # ensuring that two consecutive numbers v and w of the chain are such that either v evenly divides w or w evenly divides v
        [
            (x[i], x[i + 1]) in T for i in range(n - 1)
        ]
    )

else:
    satisfy(
        # ensuring that two consecutive numbers v and w of the chain are such that either v evenly divides w or w evenly divides v
        [
            either(
                x[i] % x[i + 1] == 0,
                x[i + 1] % x[i] == 0
            ) for i in range(n - 1)
        ]
    )

if variant("opt"):
    maximize(
        Sum(x)
    )

"""
1) Data used for the 2025 XCSP3 Competition are: [(20, 20), (20, 25), (30, 35), (30, 40), (40, 50), (40, 55), (50, 65), (50, 70), (60, 85), (60, 90), (70, 95), (70, 100), (80, 105), (80, 110)]
"""
