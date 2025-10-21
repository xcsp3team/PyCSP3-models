"""
Balanced academic curriculum problem:
  - a curriculum is a set of courses with prerequisites
  - each course must be assigned within a set number of periods
  - a course cannot be scheduled before its prerequisites
  - each course confers a number of academic credits (its 'load')
  - students have lower and upper bounds on the number of credits they can study for in a given period
  - students have lower and upper bounds on the number of courses they can study for in a given period

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011 Minizinc challenges.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Illustration
  10.json

## Model
  constraints: Sum

## Execution
  python BACP_z.py -data=<datafile.json>
  python BACP_z.py -data=<datafile.dzn> -parser=BACP_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob030/
  - https://www.researchgate.net/publication/2521521_Modelling_a_Balanced_Academic_Curriculum_Problem
  - https://webperso.info.ucl.ac.be/~pdupont/pdupont/pdf/BACP_symcon_07.pdf
  - https://www.minizinc.org/challenge/2011/results/

## Tags
  realistic, csplib, mzn10, mzn11
"""

from pycsp3 import *

nCourses, nPeriods, (load_min, load_max), (credit_min, credit_max), course_loads, prerequisites = data or load_json_data("10.json")

assert nCourses == len(course_loads)

C, P, L = range(nCourses), range(nPeriods), range(load_min, load_max + 1)

# x[c] is the period of course c (where it is assigned)
x = VarArray(size=C, dom=P)

# pc[p][c] is 1 if period p is assigned to course c
pc = VarArray(size=[P, C], dom={0, 1})

# pl[p] is the load of period p
pl = VarArray(size=P, dom=L)

# z is the value of the objective (load)
z = Var(dom=L)

satisfy(
    # determining whether periods are assigned to courses
    [pc[p][c] == (x[c] == p) for p in P for c in C],

    # respecting limits in terms of courses per period
    [Sum(pc[p]) in range(credit_min, credit_max + 1) for p in P],

    # computing period loads
    [pl[p] == course_loads * pc[p] for p in P],

    # constraining the objective value
    [pl[p] <= z for p in P],

    # enforcing prerequisites between courses
    [x[c2] < x[c1] for (c1, c2) in prerequisites],

    # implied linear constraints
    # tag(redundant)
    [
        (
            prod >= K * load_min,
            prod <= K * z
        ) for (prod, K) in [(course_loads * [x[c] > k for c in C], nPeriods - k - 1) for k in P]
    ]
)

minimize(
    z
)

""" Comments
1) One can also write:
    [pl[p] == Sum(pc[p][c] * course_loads[c] for c in C) for p in P],
 and 
    [Sum((x[x] > p) * course_loads[c] for c in C) >= (nPeriods - p - 1) * load_min for p in P], 

2) Prerequisites do not seem to be posted in the Minizinc model

3) The last group can be written as:
 [
   [course_loads * [x[c] > p for c in C] >= (nPeriods - p - 1) * load_min for p in P],
   [course_loads * [x[c] > p for c in C] <= (nPeriods - p - 1) * z for p in P]
 ]
"""
