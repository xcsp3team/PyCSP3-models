"""
This is a model for the Valve network planning for Advent of Code 2022 Day 16.
The original model has been written by Mikael Zayenz Lagerkvist for the Minizinc challenge 2023.

Instead of using different networks for varying hardness,
this model uses different planning horizons for adjusting the hardness of the problem.

## Data
  an integer (as the network is included in the model below)

## Model
  constraints: Sum, Extension, Intension, Element

## Execution
  python ValveNetwork.py -data=6

## Links
  - https://adventofcode.com/2022
  - https://github.com/zayenz/advent-of-code-2022
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

horizon = data
nNodes, nSteps = 58, horizon

# Definition of the network (this is one possible input for the problem in https://adventofcode.com/2022/day/16)

flow = cp_array(
    [14, 0, 0, 0, 0, 13, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 9, 0, 0, 0, 0, 18, 0, 0, 0, 0, 10, 12, 23, 3, 0, 8, 0, 0, 5, 0, 0, 0, 0, 0, 0, 17, 0,
     0, 0, 0, 15, 0, 4, 0, 0, 0, 0])

(GJ, HE, ET, SG, LC, EE, AA, TF, GO, QE, MI, BR, UV, EH, WK, NT, KI, AH, EL, GP, GM, LU, LB, QC, JJ, MM, VI, NV, VT, RE, FO, DV, SQ, OQ, FF, IV, HY, ML, JS, KU,
 QA, EU, SV, JG, DW, UD, QJ, HU, ZR, YA, JH, OS, LG, SB, UU, VL, AO, EM) = Nodes = range(nNodes)

connections = cp_array(
    [[UV, AO, MM, UD, GM], [QE, SV], [LU, SB], [FF, SB], [QJ, GM], [RE, BR], [QC, ZR, NT, JG, FO], [LU, MM], [LB, AH], [LG, HE], [KU, FF], [HY, EE], [GP, GJ],
     [UU, FF], [HY, EL], [FF, AA], [OQ, AO], [GO, RE], [WK, SQ], [SB, UV], [LC, GJ], [UU, DW, TF, ET, ML], [GO, VI], [ML, AA], [QJ, DV], [TF, GJ], [LB],
     [SB, KU], [HY, JG], [AH, EE], [SB, AA], [JH, UD, JJ], [EL, QA], [KI, IV, JS], [EU, NT, SG, MI, EH], [LG, OQ], [VT, BR, WK], [LU, QC], [EM, OQ],
     [MI, VL, NV, HU, DW], [OS, SQ], [FF, OS], [QJ, HE], [AA, VT], [LU, KU], [DV, GJ], [JJ, SV, LC, EM, YA], [JH, KU], [AA, VL], [QJ, OS], [HU, DV],
     [EU, YA, QA], [QE, IV], [FO, SG, NV, GP, ET], [EH, LU], [ZR, KU], [GJ, KI], [QJ, JS]])

nActions, nPersons = 2, 2
MOVE, OPEN = Actions = range(nActions)
ME, ELEPHANT = Persons = range(nPersons)

# op[i][t] is 1 if the ith node is open at time t
op = VarArray(size=[nNodes, nSteps], dom={0, 1})

# x[t][j] is the position (node) of the jth person at time t
x = VarArray(size=[nSteps, nPersons], dom=Nodes)

# ac[t][j] is the action of the jth person at time t
ac = VarArray(size=[nSteps, nPersons], dom=lambda t, j: Actions if t > 0 else None)

# cf[t] is the current flow at time t
cf = VarArray(size=nSteps, dom=range(sum(flow) + 1))

satisfy(
    # toto
    
    # computing flows
    [cf[t] == op[:, t] * flow for t in range(nSteps)],

    # setting the initial state
    [
        x[0][ME] == AA,  # AA is considered as the first node
        x[0][ELEPHANT] == AA,
        op[:, 0] == 0
    ],

    # computing open nodes
    [op[i][t] == ((ac[t][ME] == OPEN) & (x[t][ME] == i)) | ((ac[t][ELEPHANT] == OPEN) & (x[t][ELEPHANT] == i)) | op[i][t - 1]
     for t in range(1, nSteps) for i in Nodes],

    # computing the result of actions
    [IfThenElse(
        ac[t][j] == OPEN,
        Then=[
            op[x[t][j], t],
            [imply(not_belong(i, x[t]), op[i][t] == op[i][t - 1]) for i in Nodes],
            x[t][j] == x[t - 1][j]
        ],
        Else=[
            [imply(i != x[t][(j + 1) % nPersons], op[i][t] == op[i][t - 1]) for i in Nodes],
            x[t][j] in connections[x[t - 1][j]]
        ]
    ) for t in range(1, nSteps) for j in Persons]
)

maximize(
    Sum(cf)
)

# # test
# [op[i][t] == (cp_array((ac[t][ME], x[t][ME])) == (OPEN, i)) | ((ac[t][ELEPHANT] == OPEN) & (x[t][ELEPHANT] == i)) | op[i][t - 1]
#  for t in range(1, nSteps) for i in Nodes],

#     [imply(i not in x[1], op[i][1] == op[i][0]) for i in Nodes],

""" Comments
1) the form of the posted group above for computing open nodes is simpler than:
  [op[i][t] == ift(((ac[t][Me] == Open) & (x[t][Me] == i)) | ((ac[t][Elephant] == Open) & (x[t][Elephant] == i)), 1, op[i][t - 1])
      for t in range(1, nSteps) for i in Nodes],
2) note that:
    position[t][j] in connections[position[t - 1][j]]
  is equivalent to:
    (position[t - 1][j], position[t][j]) in sorted([(i, v) for i, t in enumerate(connections) for v in t])
3) note that:
    op[x[t][j], t],
  in the Then part is equivalent to:
    op[x[t][j], t] == 1,
4) note that:
    [belong(i, x[t]) | (op[i][t] == op[i][t - 1]) for i in Nodes],
  is equivalent to:    
    [imply((i != x[t][ME]) & (i != x[t][ELEPHANT]), op[i][t] == op[i][t - 1]) for i in Nodes],
   and also to:
     [imply(not_belong(i, x[t]), op[i][t] == op[i][t - 1]) for i in Nodes],
"""
