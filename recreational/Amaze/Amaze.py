"""
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line with horizontal or vertical segments,
while paying attention to not having crossed lines.

## Data Example
  simple.json

## Model
  constraints: Count, Table

## Execution
  python Amaze.py -data=<datafile.json>
  python Amaze.py -data=<datafile.json> -keep_hybrid

## Tags
  recreational, notebook
"""

from pycsp3 import *

n, m, points = data  # points[v] gives the pair of points for value v(+1)
points.insert(0, [])  # inserting a dummy entry at index 0 to simplify correspondences later
decrement(points)  # because we start indexing at 0

Fixed = [tuple(p) for pair in points for p in pair]
Values = range(1, len(points))

# x[i][j] is the value at row i and column j (possibly 0)
x = VarArray(size=[n, m], dom={0} | set(Values))

satisfy(
    # putting two initially specified occurrences of each value on the board
    [x[i][j] == v for v in Values for i, j in points[v]],

    # each cell with a fixed value has exactly one neighbour with the same value
    [
        ExactlyOne(
            within=x.beside(i, j),
            value=v
        ) for v in Values for i, j in points[v]
    ],

    # each empty/free cell either contains 0 or has exactly two neighbours with the same value
    [
        Table(
            scope=x.cross(i, j),
            supports=[(0, *[ANY] * r)] + [(v, *[v if k in (p, q) else ne(v) for k in range(r)]) for v in Values for p, q in combinations(r, 2)]
        ) for i in range(n) for j in range(m) if (i, j) not in Fixed and (r := len(x.beside(i, j)),)
    ]
)

minimize(
    Sum(x)
)

""" Comments

1) Tables contain (hybrid) conditions, which makes, for example, code more compact than:
  T = ({(0, ANY, ANY, ANY, ANY)}
      | {(v, v, v, v1, v2) for v in Values for v1 in range(nValues+1) for v2 in range(nValues+1) if v1 != v and v2 != v}
      | {(v, v, v1, v, v2) for v in Values for v1 in range(nValues+1) for v2 in range(nValues+1) if v1 != v and v2 != v}
          ...
  the hybrid conditions are automatically converted to form starred tuples except if the option -keep_hybrid is used

2) Data come from a text file via a parser that builds tuples (and not lists)
   so, we have to write tuple(p) because tuples (in data) are automatically converted to lists

3) ExactlyOne(x.beside(i, j), value=v) 
 is equivalent to:
   Count([x[i - 1][j], x[i + 1][j], x[i][j - 1], x[i][j + 1]], value=v) == 1 
   
4) Note that one can write:
 x.cross(i, j) in T
   instead of:
 Table(
    scope=x.cross(i, j),
    supports=T
 )     
"""
