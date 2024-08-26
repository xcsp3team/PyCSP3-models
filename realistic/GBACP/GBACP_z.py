"""
Generalised Balanced Academic Curriculum problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2017/2020 Minizinc challenges.
The MZN model was proposed by Jean-Noel Monette, and modified by Gustav Bjordal with help by Fatima Zohra Lebbah, Justin Pearson, and Pierre Flener.
No Licence was explicitly mentioned (MIT Licence assumed).

## Model
  constraints: BinPacking, Cardinality, Maximum, Sum

## Execution
  python GBACP_z.py -data=<datafile.dzn> -parser=GBACP_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob064/
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, csplib, mzn16, mzn17, mzn20
"""

from pycsp3 import *

nPeriods, minCourses, maxCourses, w1, w2, courseLoads, curricula, precedences, undesirables = data
nCourses, nCurricula, nPrecedences, nUndesirables = len(courseLoads), len(curricula), len(precedences), len(undesirables)

max_load = sum(courseLoads)
total_load = [sum(courseLoads[i] for i in c) for c in curricula]
ideal_load_floor = [total_load[c] // nPeriods for c in range(nCurricula)]
ideal_load_ceil = [total_load[c] // nPeriods + (0 if total_load[c] % nPeriods == 0 else 1) for c in range(nCurricula)]
distinctCurricula = [curricula[i] for i in range(nCurricula) if all(curricula[j] != curricula[i] for j in range(i))]

# x[i] is the period for the ith course
x = VarArray(size=nCourses, dom=range(nPeriods))

# l[c][p] is the load in period p of curriculum c
l = VarArray(size=[nCurricula, nPeriods], dom=range(max_load + 1))

# d[c][p] is the difference (delta) between the ideal load and the effective load in period p of curriculum c
d = VarArray(size=[nCurricula, nPeriods], dom=range(max_load + 1))

satisfy(
    # course load of all periods for each curriculum
    [
        Cardinality(
            within=x[curriculum],
            occurrences={p: range(minCourses, maxCourses + 1) for p in range(nPeriods)}
        ) for curriculum in distinctCurricula
    ],

    # respecting prerequisites
    [x[i] < x[j] for i, j in precedences],

    # computing loads
    [
        BinPacking(
            x[curricula[c]],
            sizes=courseLoads[curricula[c]],
            loads=l[c]
        ) for c in range(nCurricula)
    ],

    # computing deltas
    [d[c][p] == Maximum(l[c][p] - ideal_load_ceil[c], ideal_load_floor[c] - l[c][p]) for c in range(nCurricula) for p in range(nPeriods)]
)

minimize(
    w1 * Sum(d[c][p] * d[c][p] for c in range(nCurricula) for p in range(nPeriods)) + w2 * Sum(x[i] == j for i, j in undesirables)
)

""" Comments
1) Note that x[curriculum] is equivalent to  [x[i] fort i in curriculum]
"""
