"""
This is a generalisation of the Balanced Academic Curriculum Problem (BACP) proposed by
Marco Chiarandini, Luca Di Gaspero, Stefano Gualandi, and Andrea Schaerf at University of Udine.
See CSPLib.

## Data
  UD04.json

## Model
  Two variants compute differently the delta values:
  - a main variant involving the constraint Maximum
  - a variant 'table' involving binary table constraints

  constraints:  BinPacking, Cardinality, Maximum, Sum, Table

## Execution
  - python GBACP.py -data=<datafile.json>
  - python GBACP.py -data=<datafile.json> -variant=table

## Links
  - https://opthub.uniud.it/problem/timetabling/gbac
  - https://link.springer.com/chapter/10.1007/978-3-540-88439-2_11
  - https://www.csplib.org/Problems/prob064/
  - https://www.minizinc.org/challenge2020/results2020.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, csplib, xcsp23
"""

from pycsp3 import *

nYears, nPeriodsPerYear, loadBounds, courseLoads, curricula, precedences, undesiredPeriods = data
nPeriods, nCourses, nCurricula = nYears * nPeriodsPerYear, len(courseLoads), len(curricula)
loadRange = range(loadBounds.min, loadBounds.max + 1)

max_load = sum(courseLoads)
total_load = [sum(courseLoads[i] for i in c) for c in curricula]
ideal_floor = [total_load[c] // nPeriods for c in range(nCurricula)]
ideal_ceil = [ideal_floor[c] + (0 if total_load[c] % nPeriods == 0 else 1) for c in range(nCurricula)]
distinctCurricula = [curricula[i] for i in range(nCurricula) if all(curricula[j] != curricula[i] for j in range(i))]

# x[i] is the period for the ith course
x = VarArray(size=nCourses, dom=range(nPeriods))

# y[c][p] is the load in period p of curriculum c
y = VarArray(size=[nCurricula, nPeriods], dom=range(max_load + 1))

# d[c][p] is the difference (delta) between the ideal load and the effective load in period p of curriculum c
d = VarArray(size=[nCurricula, nPeriods], dom=range(max_load + 1))

satisfy(
    # respecting authorized loads of courses for all periods and curricula
    [
        Cardinality(
            within=x[crm],
            occurrences={p: loadRange for p in range(nPeriods)}
        ) for crm in distinctCurricula
    ],

    # respecting prerequisites
    [x[i] < x[j] for i, j in precedences],

    # computing loads
    [
        BinPacking(
            partition=x[crm],
            sizes=courseLoads[crm],
            loads=y[c]
        ) for c, crm in enumerate(curricula)
    ]
)

if not variant():
    satisfy(
        # computing deltas
        d[c][p] == Maximum(y[c][p] - ideal_ceil[c], ideal_floor[c] - y[c][p]) for c in range(nCurricula) for p in range(nPeriods)
    )

elif variant("table"):
    T = [[(max(v - ideal_ceil[c], ideal_floor[c] - v), v) for v in range(max_load + 1)] for c in range(nCurricula)]

    satisfy(
        # computing deltas
        (d[c][p], y[c][p]) in T[c] for c in range(nCurricula) for p in range(nPeriods)
    )

minimize(
    # minimizing preference violations and unbalanced loads
    Sum(d[c][p] * d[c][p] for c in range(nCurricula) for p in range(nPeriods))
    + Sum(x[i] == v + k * nPeriodsPerYear for (i, v) in undesiredPeriods for k in range(nPeriodsPerYear))
)

"""
1) options for ACE: -varh=PickOnDom -pm=3 -valh=Vals -ale=4
"""
