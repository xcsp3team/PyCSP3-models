"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data
  12-12-0-1-7.json

## Model
  constraints: Maximum, Sum

## Execution
  python EchoSched.py -data=<datafile.json>
  python EchoSched.py -data=<datafile.dzn> -parser=EchoSched_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
"""

from pycsp3 import *

durations, energies, precedences = data

nJobs, nMachines, nSpeeds = len(durations), len(durations[0]), len(durations[0][0])
J, M = range(nJobs), range(nMachines)

# x[j][m] is the starting time of the jth job on the mth machine
x = VarArray(size=[nJobs, nMachines], dom=range(sum(flatten(durations)) + 1))

# y[j][m] is the speed used for the jth job on the mth machine
y = VarArray(size=[nJobs, nMachines], dom=range(nSpeeds))

satisfy(

    # ensuring precedence constraints
    [
        x[j][v1] >= x[j][v2] + durations[j][v2][y[j][v2]] for j in J for m1 in M for m2 in M
        if m1 != m2 and (v1 := m1 if precedences[j][m1] > precedences[j][m2] else m2, v2 := m2 if v1 == m1 else m1)
    ],

    # ensuring no overlapping
    [
        either(
            x[j1][m] + durations[j1][m][y[j1][m]] <= x[j2][m],
            x[j2][m] + durations[j2][m][y[j2][m]] <= x[j1][m]
        ) for j1, j2 in combinations(nJobs, 2) for m in M
    ]
)

minimize(
    # minimizing makespan + consumed energy
    Maximum(x[j][m] + durations[j][m][y[j][m]] for j in J for m in M)
    +
    Sum(energies[j][m][y[j][m]] for j in J for m in M)
)
