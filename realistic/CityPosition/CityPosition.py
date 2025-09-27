"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  5-05.json

## Model
  constraints: Maximum, Sum

## Execution
  python CityPosition.py -data=<datafile.json>
  python CityPosition.py -data=<datafile.dzn> -parser=CityPosition_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn17
"""

from pycsp3 import *

n, roads = data
maxDistance = max(road.distance for road in roads)

# x[i] is the x-coordinate of the ith city
x = VarArray(size=n, dom=range(maxDistance + 1))

# y[i] is the y-coordinate of the ith city
y = VarArray(size=n, dom=range(maxDistance + 1))

satisfy(
    # tag(symmetry-breaking)
    [
        y[-3] == Maximum(y),
        x[-2] * 2 > x[-3] + x[-1],
        x[-1] == 0,
        y[-1] == 0
    ]
)

minimize(
    Sum(
        abs(distance * 1024 - (1007 * max(dx, dy) + 441 * min(dx, dy)))
        for (i, j, distance) in roads if (dx := abs(x[i] - x[j]), dy := abs(y[i] - y[j]))
    )
)

""" Comments
needs -di=2 with ACE
"""
