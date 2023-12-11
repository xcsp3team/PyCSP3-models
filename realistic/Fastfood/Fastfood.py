"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  02.json

## Model
  constraints: Sum, Minimum

## Execution
  python Fastfood.py -data=<datafile.json>
  python Fastfood.py -data=<datafile.dzn> -parser=Fastfood_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn11, mzn12
"""

from pycsp3 import *

nDepots, restaurants = data
positions = [r.position for r in restaurants]

# x[i] is the position of the ith depot
x = VarArray(size=nDepots, dom=positions)

satisfy(
    # depots are ordered
    x[i] < x[i + 1] for i in range(nDepots - 1)
)

minimize(
    # minimizing the sum of minimal distances of depots to restaurants
    Sum(Minimum(abs(x[i] - k) for i in range(nDepots)) for k in positions)
)
