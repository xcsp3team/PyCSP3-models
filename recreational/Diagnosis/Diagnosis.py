"""
See Problem 042 on csplib.

Model-based diagnosis can be seen as taking as input a partially parameterized structural description of a system and a set of observations about that system.
Its output is a set of assumptions which, together with the structural description, logically imply the observations,
or that are consistent with the observations.

## Data Illustration
  example.json

## Model
  constraints: Sum

## Execution
  python Diagnosis.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob042/

## Tags
  recreational, notebook, csplib
"""

from pycsp3 import *

functions, gates = data or load_json_data(
    "example.json")  # note that the two first gates are special, inserted for reserving indexes 0 and 1 (for false and true)

nGates = len(gates)

# x[i] is -1 if the ith gate is not faulty (otherwise 0 or 1 when stuck-at-0 or stuck-at-1)
x = VarArray(size=nGates, dom=lambda i: {-1} if i < 2 else {-1, 0, 1})

# y[i] is the (possibly faulty) output of the ith gate
y = VarArray(size=nGates, dom=lambda i: {i} if i < 2 else {0, 1})


def apply(gate):
    return functions[gate.f][y[gate.in1]][y[gate.in2]]


satisfy(
    # ensuring that y is coherent with the observed output
    [y[i] == j for i in range(2, nGates) if (j := gates[i].out) != -1],

    # ensuring that each gate either meets expected outputs based on its function or is broken (either stuck on or off)
    [
        If(
            y[i] != x[i],
            Then=[
                y[i] == apply(gates[i]),
                x[i] == -1
            ]
        ) for i in range(2, nGates)
    ]
)

minimize(
    # minimizing the number of faulty gates
    Sum(x[i] != -1 for i in range(2, nGates))
)
