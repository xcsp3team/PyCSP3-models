"""
The Square packing problem involves packing all squares with sizes 1 × 1 to n × n into an enclosing container.

## Data
  An integer

## Model
  constraints: Cumulative, NoOverlap

## Execution
  - python SquarePackingSuite.py -data=[number]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-85958-1_4
  - https://aaai.org/papers/icaps-06-010-optimal-rectangle-packing-a-meta-csp-approach/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, xcsp23
"""

from pycsp3 import *

n = data
assert 6 <= n <= 27  # for data (containers) below, as given in papers mentioned above

containers = [[9, 11],  # 6
              [7, 22],
              [14, 15],
              [15, 20],
              [15, 27],
              [19, 27],
              [23, 29],
              [22, 38],
              [23, 45],
              [23, 55],
              [27, 56],
              [39, 46],
              [31, 69],
              [47, 53],
              [34, 85],
              [38, 88],
              [39, 98],
              [64, 68],
              [56, 88],
              [43, 129],
              [70, 89],
              [47, 148]]  # 27

# initial reduction as indicated in the first paper cited above
t = [[], [1, 2], [2, 3], [2]] + [[3]] * 4 + [[4]] * 3 + [[5]] * 6 + [[6]] * 4 + [[7]] * 8 + [[8]] * 5 + [[9]] * 11 + [[10]]

width, height = containers[n - 6]

# x[i] is the x-coordinate where is put the ith rectangle
x = VarArray(size=n, dom=lambda i: range(width - i))

# y[i] is the y-coordinate where is put the ith rectangle
y = VarArray(size=n, dom=lambda i: range(height - i))

satisfy(
    # no overlap on boxes
    NoOverlap(origins=[(x[i], y[i]) for i in range(n)], lengths=[(i + 1, i + 1) for i in range(n)]),

    # tag(redundant-constraints)
    [
        Cumulative(
            Task(origin=x[i], length=i + 1, height=i + 1) for i in range(n)
        ) <= height,

        Cumulative(
            Task(origin=y[i], length=i + 1, height=i + 1) for i in range(n)
        ) <= width
    ],

    # tag(symmetry-breaking)
    (
        [x[-1] <= (width - n) // 2, y[-1] <= (height - n) // 2],

        [x[i] != v for i in range(n) for v in t[i]],
        [y[i] != v for i in range(n) for v in t[i]]
    ),
    # (
    #     [(y[i] > y[j]) | (y[j] - y[i] > (i - j)) | (x[j] - x[i] - (i + 1) not in t[j]) for i in range(n) for j in range(i) if len(t[j]) > 0],
    #     [(x[i] > x[j]) | (x[j] - x[i] > (i - j)) | (y[j] - y[i] - (i + 1) not in t[j]) for i in range(n) for j in range(i) if len(t[j]) > 0]
    # )
)

""" Comments
1) it is better to precisely define initial domains (rather than posting unary constraints)
so as to let informed the global constraints NoOverlap (and Cumulative)
"""
