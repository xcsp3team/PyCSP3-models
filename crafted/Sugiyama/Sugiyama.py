"""
Optimal ordering layout for a Sugiyami style graph.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  g3-8-8-2.json

## Model
  constraints: AllDifferent, Count, Sum

## Execution
  python Sugiyama.py -data=<datafile.json>
  python Sugiyama.py -data=<datafile.dzn> -parser=Sugiyama_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Layered_graph_drawing
  - https://www.minizinc.org/challenge2010/results2010.html

## Tags
  crafted, mzn10
"""

from pycsp3 import *

widths, n, edges = data
src, dst = zip(*edges)
nLayers, e = len(widths), len(src)

layers = [range(sum(widths[:i]), sum(widths[:i + 1])) for i in range(nLayers)]
starts = [{src[e] for e in range(e) if dst[e] == i} for i in range(n)]
ends = [{dst[e] for e in range(e) if src[e] == i} for i in range(n)]
unconnected = [[i for i in layer if len(starts[i]) == len(ends[i]) == 0] for layer in layers]

fully_connected = [{n1, n2, n3, n4} for n1 in range(n) for n2 in ends[n1] for n3 in starts[n2] if n1 < n3 for n4 in ends[n1] if n4 in ends[n3] and n2 < n4]
crossings = [(e1, e2) for layer in layers[:-1] for e1, e2 in combinations(e, 2) if src[e1] != src[e2] and dst[e1] != dst[e2]
             and src[e1] in layer and src[e2] in layer and all(t != {src[e1], src[e2], dst[e1], dst[e2]} for t in fully_connected)]
nCrossings = len(crossings)


def compatible(t1, t2):
    return [(n1, n2) for layer in layers for n1 in layer for n2 in layer if n1 != n2 and (len(t1[n1]) == 0 or len(t1[n2]) == 0)
            and len(t2[n1] & t2[n2]) <= 1 < len(t2[n1] | t2[n2]) and len(t2[n1]) != 0 and len(t2[n2]) != 0]


# x|i] is the position of the ith node
x = VarArray(size=n, dom=range(n))

# y[j] is 1 if the jth crossing is effective
y = VarArray(size=nCrossings, dom={0, 1})

satisfy(
    # putting nodes in the right layers
    [x[i] in layer for layer in layers for i in layer],

    # nodes are in different positions in each layer
    [AllDifferent(x[layer]) for layer in layers],

    # computing crossings
    [
        y[j] == both(
            x[src[e1]] < x[src[e2]],
            x[dst[e2]] < x[dst[e1]])
        + both(
            x[src[e2]] < x[src[e1]],
            x[dst[e1]] < x[dst[e2]]
        ) for j, (e1, e2) in enumerate(crossings)
    ],

    # putting unconnected nodes first on each layer
    [x[j] == sum(widths[:i]) + k for i in range(nLayers) for k, j in enumerate(unconnected[i])],

    [
        If(
            AllHold(x[n3] < x[n4] for n3 in starts[n1] for n4 in starts[n2] if n3 != n4),
            Then=x[n1] < x[n2]
        ) for n1, n2 in compatible(ends, starts)
    ],
    [
        If(
            AllHold(x[n3] < x[n4] for n3 in ends[n1] for n4 in ends[n2] if n3 != n4),
            Then=x[n1] < x[n2]
        ) for n1, n2 in compatible(starts, ends)
    ]
)

minimize(
    # minimizing crossings
    Sum(y)
)

""" Comments
1) [AllDifferent(x[layer]) for layer in layers]
     is a shortcut for:
   [AllDifferent(x[i] for i in layer) for layer in layers]
"""
