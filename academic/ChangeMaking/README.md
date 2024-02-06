# Problem ChangeMaking

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

  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python ChangeMaking.py -data=number
  - python ChangeMaking.py -data=number -variant=compact

## Links
  - https://en.wikipedia.org/wiki/Change-making_problem

## Tags
  academic
