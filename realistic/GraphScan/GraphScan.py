"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The original model seems to have been written by Peter Schneider-Kamp (MIT Licence assumed).

## Data
  n10-p1500-c15.json

## Model
  constraints: AllDifferent, Count, Element, Maximum

## Execution
  python GraphScan.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

edges, reverse, length, succ, n, scanmultiplier = data
decrement([edges, reverse, succ])
nEdges, nDrones = len(edges), n
assert edges[0] == 0 and all(edges[i + 1] == edges[i] + 1 for i in range(nEdges - 1))

makespan = (sum(length) * (scanmultiplier + 1)) // n
END = nEdges

next = VarArray(size=[nDrones, nEdges + 1], dom=range(nEdges + 1))  # next edge after this one
visit = VarArray(size=[nDrones, nEdges + 1], dom=range(makespan + 1))  # when edge was started traversal
scan = VarArray(size=[nDrones, nEdges], dom={0, 1})  # did this drone scan the edge
traverse = VarArray(size=[nDrones, nEdges], dom=lambda d, e: {length[e], scanmultiplier * length[e]})

endtime = Var(range(makespan + 1))

satisfy(
    [traverse[d][e] == (scan[d, e] * (scanmultiplier - 1) + 1) * length[e] for d in range(nDrones) for e in range(nEdges)],

    # The next is either a reachable edge, the same edge (meaning not used) or end
    [next[d, e] in succ[e] + [e, END] for d in range(nDrones) for e in range(nEdges)],
    [next[d, -1] != END for d in range(nDrones)],

    # FORCE END TO POINT AT THE START OF THE TOUR
    [AllDifferent(next[d]) for d in range(nDrones)],

    # scan edges must be traversed
    [
        If(
            scan[d][e],
            Then=next[d][e] != e
        ) for d in range(nDrones) for e in range(nEdges)
    ],

    # visit time increases as we go
    [
        If(
            next[d][e] == e,
            Then=visit[d][e] == makespan
        ) for d in range(nDrones) for e in range(nEdges)
    ],

    [
        If(
            next[d][e] != e,
            Then=visit[d, next[d][e]] == visit[d][e] + traverse[d][e]
        ) for d in range(nDrones) for e in range(nEdges)
    ],

    # REPLACEMENT
    [visit[d, next[d, END]] == 0 for d in range(nDrones)],
    [traverse[d][e] + traverse[d][reverse[e]] <= (scanmultiplier + 1) * length[e] for d in range(nDrones) for e in range(nEdges)],
    [either(scan[d][e], next[d][e] != reverse[e]) for d in range(nDrones) for e in range(nEdges)],

    #  every edge is scanned
    [Exist(either(scan[d, e], scan[d, reverse[e]]) for d in range(nDrones)) for e in range(nEdges)],

    [either(scan[d, e] == 0, scan[d, reverse[e]] == 0) for d in range(nDrones) for e in range(nEdges)],

    endtime == Maximum(visit[:, END])
)

minimize(
    endtime
)
