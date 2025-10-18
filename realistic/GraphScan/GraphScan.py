"""
Problem of global coverage-path planning for linear-infrastructure inspection using multiple autonomous UAVs (Autonomous unmanned aerial vehicles, or drones).
The problem is mathematically formulated as a variant of the Min–Max K-Chinese Postman Problem (MM K-CPP) with multi-weight edges.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge (directory multi-agent-graph-coverage).
The original MZN model seems to have been written by Peter Schneider-Kamp (MIT Licence assumed).

## Data
  n10-p1500-c15.json

## Model
  constraints: AllDifferent, Count, Element, Maximum

## Execution
  python GraphScan.py -data=<datafile.json>

## Links
  - https://findresearcher.sdu.dk/ws/portalfiles/portal/241768335/drones_07_00563.pdf
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn23
"""

from pycsp3 import *

edges, reverse, length, successors, n, scan_multiplier = data or load_json_data("n10-p1500-c15.json")

decrement([edges, reverse, successors])

nEdges, nDrones = len(edges), n
E, D = range(nEdges), range(nDrones)

assert edges[0] == 0 and all(edges[i + 1] == edges[i] + 1 for i in range(nEdges - 1))

makespan = (sum(length) * (scan_multiplier + 1)) // n
END = nEdges

next = VarArray(size=[nDrones, nEdges + 1], dom=range(nEdges + 1))  # next edge after this one

visit = VarArray(size=[nDrones, nEdges + 1], dom=range(makespan + 1))  # when edge was started traversal

scan = VarArray(size=[nDrones, nEdges], dom={0, 1})  # did this drone scan the edge

traverse = VarArray(size=[nDrones, nEdges], dom=lambda d, e: {length[e], scan_multiplier * length[e]})

endtime = Var(range(makespan + 1))

satisfy(
    [traverse[d][e] == (scan[d][e] * (scan_multiplier - 1) + 1) * length[e] for d in D for e in E],

    # The next is either a reachable edge, the same edge (meaning not used) or end
    [next[d][e] in successors[e] + [e, END] for d in D for e in E],
    [next[d][-1] != END for d in D],

    # FORCE END TO POINT AT THE START OF THE TOUR
    [AllDifferent(next[d]) for d in D],

    # scan edges must be traversed
    [
        If(
            scan[d][e],
            Then=next[d][e] != e
        ) for d in D for e in E
    ],

    # visit time increases as we go
    [
        If(
            next[d][e] == e,
            Then=visit[d][e] == makespan
        ) for d in D for e in E
    ],

    [
        If(
            next[d][e] != e,
            Then=visit[d, next[d][e]] == visit[d][e] + traverse[d][e]
        ) for d in D for e in E
    ],

    # REPLACEMENT
    [visit[d][next[d][END]] == 0 for d in D],
    [traverse[d][e] + traverse[d][reverse[e]] <= (scan_multiplier + 1) * length[e] for d in D for e in E],
    [either(scan[d][e], next[d][e] != reverse[e]) for d in D for e in E],

    #  every edge is scanned
    [
        Exist(either(scan[d][e], scan[d][reverse[e]]) for d in D)
        for e in E
    ],

    [either(scan[d][e] == 0, scan[d][reverse[e]] == 0) for d in D for e in E],

    endtime == Maximum(visit[:, END])
)

minimize(
    endtime
)
