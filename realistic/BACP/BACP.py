"""
Problem 30 in CSPLib.

BACP is to design a balanced academic curriculum by assigning periods to courses in a way that the academic load of each period is balanced,
i.e., as similar as possible.

## Data Example
  10.json

## Model
  There are two variants:
   - one with extension constraints
   - one with intension constraints
  and one subvariant "d"

  constraints: Count, Minimum, Maximum, Sum, Table

## Execution
  python BACP.py -data=<datafile.json> -variant=m1
  python BACP.py -data=<datafile.json> -variant=m2
  python BACP.py -data=<datafile.json> -variant=m1-d
  python BACP.py -data=<datafile.json> -variant=m2-d

## Links
 - https://www.csplib.org/Problems/prob030/
 - https://www.researchgate.net/publication/2521521_Modelling_a_Balanced_Academic_Curriculum_Problem
 - https://webperso.info.ucl.ac.be/~pdupont/pdupont/pdf/BACP_symcon_07.pdf

## Tags
  realistic, notebook, csplib
"""

from pycsp3 import *

assert (variant("m1") or variant("m2")) and (not subvariant() or subvariant("d"))

nCourses, nPeriods, (minCredits, maxCredits), (minCourses, maxCourses), credits, prerequisites = data or load_json_data("10.json")

assert nCourses == len(credits)
maxCredits = maxCredits * maxCourses if subvariant("d") else maxCredits

C, P = range(nCourses), range(nPeriods)

# s[c] is the period (schedule) for course c
s = VarArray(size=nCourses, dom=range(nPeriods))

# co[p] is the number of courses at period p
co = VarArray(size=nPeriods, dom=range(minCourses, maxCourses + 1))

# cr[p] is the number of credits at period p
cr = VarArray(size=nPeriods, dom=range(minCredits, maxCredits + 1))

if variant("m1"):
    def table(c):
        return {(0,) * p + (credits[c],) + (0,) * (nPeriods - p - 1) + (p,) for p in P}


    # cp[c][p] is 0 if the course c is not planned at period p, the number of credits for c otherwise
    cp = VarArray(size=[nCourses, nPeriods], dom=lambda c, p: {0, credits[c]})

    satisfy(
        # channeling between arrays cp and s
        [(cp[c], s[c]) in table(c) for c in C],

        # counting the number of courses in each period
        [Count(within=s, value=p) == co[p] for p in P],

        # counting the number of credits in each period
        [Sum(cp[:, p]) == cr[p] for p in P]
    )

elif variant("m2"):
    # pc[p][c] is 1 iff the course c is at period p
    pc = VarArray(size=[nPeriods, nCourses], dom={0, 1})

    satisfy(
        # tag(channeling)
        [pc[p][c] == (s[c] == p) for p in P for c in C],

        # ensuring that each course is assigned to a period
        [Sum(pc[:, c]) == 1 for c in C],

        # counting the number of courses in each period
        [Sum(pc[p]) == co[p] for p in P],

        # counting the number of credits in each period
        [pc[p] * credits == cr[p] for p in P]
    )

satisfy(
    # handling prerequisites
    s[c2] < s[c1] for (c1, c2) in prerequisites
)

if subvariant("d"):
    minimize(
        # minimizing the maximal distance in terms of credits
        Maximum(cr) - Minimum(cr)
    )
else:
    minimize(
        # minimizing the maximum number of credits in periods
        Maximum(cr)
    )

annotate(decision=s)

""" Comments
1) The way we build the table could also be written as:
 return {tuple(credits[c] if j == p else p if j == nPeriods else 0 for j in range(nPeriods + 1)) for p in P}
"""
