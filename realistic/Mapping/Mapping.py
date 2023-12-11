"""
Mapping an H263 encoder on a system with a network on chip/
This is a simplified version of the model presented in the paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Krzysztof Kuchcinski.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  mesh2x2-2.json

## Model
  constraints: BinPacking, Count, Flow, Maximum, Sum

## Execution
  python Mapping.py -data=<datafile.json>
  python Mapping.py -data=<datafile.dzn> -parser=Mapping_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0045790614002286
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn15, mzn16, mzn18, mzn21
"""

from pycsp3 import *
from pycsp3.problems.data.parsing import split_with_rows_of_size

nProcessors, nLinks, bandwidth, src_dst, inStreams, processorLoad, actorLoads, arcs = data
nFlows = len(src_dst)

n, m = nProcessors + 2, len(arcs)  # n is the number of nodes
assert m == nLinks + 2 * nProcessors
MAX = 10000

balance = [[0] * nProcessors + [inStreams[i], -inStreams[i]] for i in range(nFlows)]
total_balance = [0] * nProcessors + [inStreams[i] for i in range(nFlows)] + [-inStreams[i] for i in range(nFlows)]

unit = [0] * nProcessors + [1] * nLinks + [0] * nProcessors
total_unit = [0] * nFlows * nProcessors + [1] * nLinks + [0] * nFlows * nProcessors

in_cons = [nProcessors + 1 + i // (2 * nProcessors) if i % 2 == 0 else (i // 2) % nProcessors + 1 for i in range(2 * nFlows * nProcessors)]
out_cons = [(i // 2) % nProcessors + 1 if i % 2 == 0 else nProcessors + nFlows + 1 + i // (2 * nProcessors) for i in range(2 * nFlows * nProcessors)]
all_connections = split_with_rows_of_size(in_cons + [arcs[i][j] for i in range(nProcessors, nLinks + nProcessors) for j in range(2)] + out_cons, 2)

loads = [0 if any(src_dst[i][j] in src_dst[k] for k in range(i)) else actorLoads[src_dst[i][j] - 1] for j in range(2) for i in range(nFlows)]
flowing = [[(j, n) for j in range(nFlows) for n in range(nProcessors, nLinks + nProcessors) if arcs[n][0] - 1 == i] for i in range(nProcessors)]

# x[i] is the load of the ith processor
x = VarArray(size=nProcessors, dom=range(processorLoad + 1))

# flow_cost[k] is the cost of the kth flow
flow_cost = VarArray(size=nFlows, dom=range(MAX + 1))

# comm_cost is the communication cost of the global flow
comm_cost = Var(dom=range(MAX + 1))

# p[i] is the processor used for the ith (double) flow
p = VarArray(size=2 * nFlows, dom=range(nProcessors))

# lf[i] is the flow from the ith link
lf = VarArray(size=nLinks, dom=range(bandwidth + 1))

# pf[i] is the flow out from the ith processor
pf = VarArray(size=nProcessors, dom=range(5 * bandwidth + 1))

# y[k][j] is the value of the kth flow on the jth arc
y = VarArray(size=[nFlows, m], dom=range(max(max(inStreams), bandwidth) + 1))

total_flow = VarArray(size=[2 * nProcessors * nFlows + nLinks], dom=range(max(max(inStreams), bandwidth) + 1))

satisfy(
    # handling incoming and outgoing streams
    [
        (
            Count(y[i][:nProcessors], value=0) == nProcessors - 1,
            Count(y[i][- nProcessors:], value=0) == nProcessors - 1
        ) for i in range(nFlows)
    ],

    # computing flows
    [
        [Flow(y[i], balance=balance[i], arcs=arcs, weights=unit) == flow_cost[i] for i in range(nFlows)],
        Flow(total_flow, balance=total_balance, arcs=all_connections, weights=total_unit) == comm_cost,
        [lf[i] >= Sum(y[:, i + nProcessors]) for i in range(nLinks)]
    ],

    # determining which processors are used
    [
        (
            (y[i][j] != 0) == (p[i] == j),
            (y[i][- nProcessors + j] != 0) == (p[nFlows + i] == j)
        ) for i in range(nFlows) for j in range(nProcessors)
    ],

    # computing loads of processors
    BinPacking(p, sizes=loads, loads=x),

    # computing flow out for each processor
    [pf[i] == Sum(y[j][n] for j, n in flowing[i]) for i in range(nProcessors)],

    # about flow processors
    [
        [p[i] == p[j] for i in range(nFlows) for j in range(i + 1, nFlows) if src_dst[i][0] == src_dst[j][0]],
        [p[i] == p[nFlows + j] for i in range(nFlows) for j in range(nFlows) if src_dst[i][0] == src_dst[j][1]],
        [p[nFlows + i] == p[nFlows + j] for i in range(nFlows) for j in range(i + 1, nFlows) if src_dst[i][1] == src_dst[j][1]]
    ]
)

minimize(
    Maximum(x[i] + Sum((p[src_dst[j][0] - 1] == i) * flow_cost[j] for j in range(nFlows)) for i in range(nProcessors))
)

"""
1) Variables inFlow, outFlow and commFlow of the initial model are not connected (and so, not introduced here)
 inFlow = VarArray(size=[nFlows, k], dom=lambda i, j: {0, inStream[i]})  
 outFlow = VarArray(size=[nFlows, k], dom=lambda i, j: {0, inStream[i]})  
 commFlow = VarArray(size=[nFlows, nLinks], dom=range(link_bandwidth + 1))
"""
