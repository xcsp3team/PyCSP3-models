"""
Automatic layout of tables is useful in word processing applications.
When the table contains text, minimizing the height of the table for a fixed maximum width is a difficult combinatorial optimization problem.
See links to papers below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

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
  - https://www.minizinc.org/challenge2011/results2011.html

## Tags
  realistic, mzn11, mzn23
"""

from pycsp3 import *

pixelWidth, nConfigurations, n, m, widths, heights = data

minWidth, maxWidth = max(0, min(flatten(widths))), max(flatten(widths))
minHeight, maxHeight = max(0, min(flatten(heights))), max(flatten(heights))

rangeWidth, rangeHeight = range(minWidth, maxWidth + 1), range(minHeight, maxHeight + 1)
indexes = [(i, j) for i in range(n) for j in range(m)]

# x[i][j] is the configuration used for the pixel at coordinates (i,j)
x = VarArray(size=[n, m], dom=range(nConfigurations))

# cw[i,j] is the width of cell at i,j
cw = VarArray(size=[n, m], dom=rangeWidth)

# ch[i,j] is the height of cell at i,j
ch = VarArray(size=[n, m], dom=rangeHeight)

# h[i] is the height of row i
h = VarArray(size=n, dom=rangeHeight)

# w[j] is the width of column j
w = VarArray(size=m, dom=rangeWidth)

satisfy(
    pixelWidth >= Sum(w),

    # ensuring that the heights of rows are sufficiently large
    [h[i] >= ch[i][j] for i, j in indexes],

    # ensuring that the widths of columns are sufficiently large
    [w[j] >= cw[i][j] for i, j in indexes],

    # computing the widths of cells
    [cw[i][j] == widths[i][j][x[i][j]] for i, j in indexes],

    # computing the heights of cells
    [ch[i][j] == heights[i][j][x[i][j]] for i, j in indexes]
)

minimize(
    # minimizing total height
    Sum(h)
)
