"""
Shortest Path Problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
The MZN model was proposed by Jakob Puchinger.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  00.json

## Model
  constraints: Sum

## Execution
  python ShortestPath.py -data=<datafile.json>
  python ShortestPath.py -data=<datafile.dzn> -parser=ShortestPath_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  crafted, mzn08
"""

from pycsp3 import *

n, edges, start, end = data or load_json_data("00.json")

src, dst, lgt = zip(*edges)
m = len(edges)


def select(t, j):
    return (x[i] for i in range(m) if t[i] == j)


# x[i] is 1 if the ith edge is used
x = VarArray(size=m, dom={0, 1})

satisfy(
    Sum(select(src, start)) - Sum(select(dst, start)) == 1,

    Sum(select(src, end)) - Sum(select(dst, end)) == -1,

    [Sum(select(src, j)) - Sum(select(dst, j)) == 0 for j in range(n) if j not in (start, end)]
)

minimize(
    x * lgt
)
