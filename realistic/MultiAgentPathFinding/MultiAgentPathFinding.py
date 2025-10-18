"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2022 Minizinc challenges.
The original MZN model was proposed by Hakan Kjellerstrand, after translating the one by Neng-Fa Zhou in Picat
- no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  g16-p20-a20.json

## Model
  constraints: AllDifferent, Maximum, Sum, Table

## Execution
  python MultiAgenPathFinding.py -data=<datafile.json>
  python MultiAgenPathFinding.py -variant=table -data=<datafile.json>
  python MultiAgentPathFinding.py -data=<datafile.dzn> -parser=MultiAgentPathFinding_ParserZ.py

## Links
  - https://ieeexplore.ieee.org/document/8372050
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn17, mzn22
"""

from pycsp3 import *

assert not variant() or (variant("table") and (not subvariant() or subvariant("mks")))

agents, horizon, neighbors, = data or load_json_data("g16-p20-a20.json*")

# horizon +=10 for testing
src, dst = zip(*agents)

nAgents, nNodes = len(agents), len(neighbors)
A, N = range(nAgents), range(nNodes)

# assert all(agent[0] != agent[1] for agent in agents)  # not necessarily true (as seen in one instance in mzn 22)

if not variant():

    # s[t][a][i] is 1 if at time t, the agent a is at node i
    s = VarArray(size=[horizon + 1, nAgents, nNodes], dom={0, 1})

    # e[a] is the time when the agent a arrives at its destination
    e = VarArray(size=nAgents, dom=range(horizon + 1))

    # x[t][a] is the node where is the agent a at time t
    x = VarArray(size=[horizon + 1, nAgents], dom=range(nNodes))

    # y[t][a] is 1 if the agent a has finished at time t
    y = VarArray(size=[horizon + 1, nAgents], dom={0, 1})

    satisfy(
        # computing the status at any time
        [s[t][a][i] == (x[t][a] == i) for t in range(horizon + 1) for a in A for i in N],

        # setting positions of agents
        (
            [s[0][a][src[a]] == 1 for a in A],
            [s[-1][a][dst[a]] == 1 for a in A]
        ),

        # each agent occupies exactly one node at each time
        [Sum(s[t][a]) == 1 for t in range(horizon + 1) for a in A],

        # no two agents occupy the same node at any time
        [Sum(s[t, :, i]) <= 1 for t in range(horizon + 1) for i in N],

        # every transition is valid
        [
            If(
                s[t][a][i],
                Then=disjunction(s[t + 1][a][j] == 1 for j in neighbors[i])  # using Exist instead is inefficient (too many aux variables)
            ) for t in range(horizon) for a in A for i in N
        ],

        # computing when it is finished for agents
        (
            [y[t][a] == (e[a] == t) for t in range(horizon + 1) for a in A],
            [
                If(
                    y[t][a],
                    Then=[
                        s[t - 1][a][dst[a]] == 0,
                        [s[t1][a][dst[a]] == 1 for t1 in range(t, horizon + 1)]
                    ]
                ) for t in range(1, horizon + 1) for a in A
            ]
        ),

        # agents can't occupy the same node at the same time
        [AllDifferent(x[t]) for t in range(horizon + 1)],

        # once the agent is at its destination it stays there
        [
            If(
                x[t][a] == dst[a],
                Then=x[t + 1][a] == dst[a]
            ) for t in range(horizon) for a in A
        ],

        # source node of agent
        x[0] == src,

        # target node of agent
        x[-1] == dst,

        # end times of the agent
        [
            e[a] == Sum((t + 1) * both(s[t][a][dst[a]] == 0, s[t + 1][a][dst[a]] == 1) for t in range(1, horizon)) + s[0][a][dst[a]]
            for a in A
        ]
    )

    minimize(
        Sum(e) + nAgents
    )

elif variant("table"):

    T = [(i, v) for i, t in enumerate(neighbors) for v in t]

    # x[t][a] is the node where is the agent a at time t
    x = VarArray(size=[horizon + 1, nAgents], dom=range(nNodes))

    # e[a] is the time when the agent a arrives at its destination
    e = VarArray(size=nAgents, dom=range(horizon + 1))

    satisfy(
        # agents must occupy different node at any time
        [AllDifferent(x[t]) for t in range(horizon + 1)],

        # agents at their destinations stays there
        [
            If(
                x[t][a] == dst[a],
                Then=x[t + 1][a] == dst[a]
            ) for t in range(horizon) for a in A
        ],

        # agents can only move to connected nodes
        [(x[t][a], x[t + 1][a]) in T for t in range(horizon) for a in A],

        # setting agents at their initial positions
        x[0] == src,

        # setting agents at their final positions
        x[-1] == dst,

        # computing end times of agents
        [(e[a] == t + 1) == both(x[t][a] != dst[a], x[t + 1][a] == dst[a]) for t in range(horizon) for a in A]
    )

    if subvariant("mks"):
        minimize(
            Maximum(e)
        )
    else:
        minimize(
            Sum(e) + nAgents
        )

""" Comments
1) Using SAC3 as preprocessing allows us to solve efficiently the 5 minizinc instances for variant 'table'
"""
