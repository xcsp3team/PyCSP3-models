"""
The change-making problem addresses the question of finding the minimum number of coins (of certain denominations) that
add up to a given amount of money. It is a special case of the integer knapsack problem, and has applications wider than
just currency.
It is also the most common variation of the coin change problem, a general case of partition in which, given the
available denominations of an infinite set of coins, the objective is to find out the number of possible ways
of making a change for a specific amount of money, without considering the order of the coins.

### Example
  For n=13, one needs at least 4 coins:
  ``` 13 = 3x1 + 10```

## Data
  a number n, the given amount of money

## Model
  There are two variants: a main one and a compact one (with fewer variables).

  constraints: Sum

## Execution
  - python ChangeMaking.py -data=number
  - python ChangeMaking.py -data=number -variant=compact

## Links
  - https://en.wikipedia.org/wiki/Change-making_problem

## Tags
  academic
"""

from pycsp3 import *

k = data or 13

if not variant():
    # c1 is the number of coins of 1 cent
    c1 = Var(range(50))

    # c5 is the number of coins of 5 cents
    c5 = Var(range(50))

    # c10 is the number of coins of 10 cents
    c10 = Var(range(50))

    # c20 is the number of coins of 20 cents
    c20 = Var(range(50))

    # c50 is the number of coins of 50 cents
    c50 = Var(range(50))

    # e1 is the number of coins of 1 euro
    e1 = Var(range(50))

    # e2 is the number of coins of 2 euros
    e2 = Var(range(50))

    satisfy(
        # the given change must be correct
        [c1, c5, c10, c20, c50, e1, e2] * [1, 5, 10, 20, 50, 100, 200] == k
    )

    minimize(
        # the given change must have the minimum number of coins
        c1 + c5 + c10 + c20 + c50 + e1 + e2
    )

elif variant("compact"):
    # coins[i] is the number of coins of the ith type
    coins = VarArray(size=7, dom=range(50))

    satisfy(
        # the given change must be correct
        coins * [1, 5, 10, 20, 50, 100, 200] == k
    )

    minimize(
        # the given change must have the minimum number of coins
        Sum(coins)
    )
