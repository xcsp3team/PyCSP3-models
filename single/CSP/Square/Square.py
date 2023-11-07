"""
See http://en.wikibooks.org/wiki/Puzzles/Arithmetical_puzzles/Digits_of_the_Square

There is one four-digit whole number x, such that the last four digits of x^2
are in fact the original number x. What is it?

## Data
all integrated (single instance)

## Execution
  python3 Square.py

## Links
 - http://en.wikibooks.org/wiki/Puzzles/Arithmetical_puzzles/Digits_of_the_Square

## Tags
  single
"""

from pycsp3 import *

# x is the number we look for
x = Var(range(1000, 10000))

# d[i] is the ith digit of x
d = VarArray(size=4, dom=range(10))

satisfy(
    d * [1000, 100, 10, 1] == x,

    (x * x) % 10000 == x
)
