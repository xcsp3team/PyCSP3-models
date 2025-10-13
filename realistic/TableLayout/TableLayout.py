"""
Automatic layout of tables is useful in word processing applications.
When the table contains text, minimizing the height of the table for a fixed maximum width is a difficult combinatorial optimization problem.
See links to papers below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  1000-1615-479.json

## Model
  constraints: Element, Sum, Table

## Execution
  python TableLayout.py -data=<datafile.json>
  python TableLayout.py -data=<datafile.dzn> -parser=TableLayout_ParserZ.py

## Links
  - https://dl.acm.org/doi/abs/10.1145/2034691.2034697
  - https://pubsonline.informs.org/doi/10.1287/ijoc.2014.0637
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn11, mzn23
"""

from pycsp3 import *

pixel_width, nConfigurations, n, m, widths, heights = data or load_json_data("1000-1615-479.json")

range_width = range(max(0, min(W := flatten(widths))), max(W) + 1)
range_height = range(max(0, min(H := flatten(heights))), max(H) + 1)

P = [(i, j) for i in range(n) for j in range(m)]

# x[i][j] is the configuration used for the pixel at coordinates (i,j)
x = VarArray(size=[n, m], dom=range(nConfigurations))

# cw[i,j] is the width of cell at i,j
cw = VarArray(size=[n, m], dom=range_width)

# ch[i,j] is the height of cell at i,j
ch = VarArray(size=[n, m], dom=range_height)

# w[j] is the width of column j
w = VarArray(size=m, dom=range_width)

# h[i] is the height of row i
h = VarArray(size=n, dom=range_height)

satisfy(
    pixel_width >= Sum(w),

    # ensuring that the heights of rows are sufficiently large
    [h[i] >= ch[i][j] for i, j in P],

    # ensuring that the widths of columns are sufficiently large
    [w[j] >= cw[i][j] for i, j in P],

    # computing the widths of cells
    [cw[i][j] == widths[i][j][x[i][j]] for i, j in P],

    # computing the heights of cells
    [ch[i][j] == heights[i][j][x[i][j]] for i, j in P]
)

minimize(
    # minimizing total height
    Sum(h)
)
