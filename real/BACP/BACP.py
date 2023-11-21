"""
Balanced academic curriculum problem:
  - a curriculum is a set of courses with prerequisites
  - each course must be assigned within a set number of periods
  - a course cannot be scheduled before its prerequisites
  - each course confers a number of academic credits (its 'load')
  - students have lower and upper bounds on the number of credits they can study for in a given period
  - students have lower and upper bounds on the number of courses they can study for in a given period

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01.json

## Model
  constraints: Sum

## Execution
  python BACP.py -data=<datafile.json>
  python BACP.py -data=<datafile.dzn> -parser=BACP_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob030/
  - https://www.minizinc.org/challenge2011/results2011.html

## Tags
  real, csplib, mzn10, mzn11
"""

from pycsp3 import *

nPeriods, l_lb, l_ub, c_lb, c_ub, loads, prerequisites = data
nCourses = len(loads)

C, P, L = range(nCourses), range(nPeriods), range(l_lb, l_ub + 1)

# x[i] is the period where is assigned the ith course
x = VarArray(size=nCourses, dom=P)

# pd[k][i] is 1 if the kth period is assigned to the ith course
pd = VarArray(size=[nPeriods, nCourses], dom={0, 1})

# ld[k] is the load of the kth period
ld = VarArray(size=nPeriods, dom=L)

# z is the value of the objective (load)
z = Var(dom=L)

satisfy(
    # determining whether periods are assigned to courses
    [pd[k][i] == (x[i] == k) for k in P for i in C],

    # respecting limits in terms of courses per period
    [Sum(pd[k]) in range(c_lb, c_ub + 1) for k in P],

    # computing period loads
    [ld[k] == loads * pd[k] for k in P],

    # constraining the objective value
    [ld[k] <= z for k in P],

    # enforcing prerequisites between courses
    [x[j] < x[i] for (i, j) in prerequisites],

    # implied linear constraints  tag(redundant-constraints)
    [
        (
            prod >= K * l_lb,
            prod <= K * z
        ) for (prod, K) in ((loads * [x[i] > k for i in C], nPeriods - k - 1) for k in P)
    ]
)

minimize(
    z
)

""" Comments
1) One can also write:
    [ld[k] == Sum(pd[kl][i] * loads[i] for i in C) for k in P],
 and 
    [Sum((x[i] > k) * loads[i] for i in C) >= (nPeriods - k - 1) * l_lb for k in P], 

2) prerequisites do not seem to be posted in the Minizinc model

3) the last group can be written as:
 [
   [loads * [x[i] > k for i in C] >= (nPeriods - k - 1) * l_lb for k in P],
   [loads * [x[i] > k for i in C] <= (nPeriods - k - 1) * z for k in P]
 ]
"""
