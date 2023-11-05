"""
Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).
The objective is to find an optimal schedule so that tasks start as close as possible to the given start time for each task,
penalizing earliness or tardiness according to the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by the University of Melbourne and NICTA.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  j30-27-5-3.json

## Model
  constraints: Count, Cumulative, Sum

## Execution
  python RCPSPWetDiverse.py -data=<datafile.json>
  python RCPSPWetDiverse.py -data=<datafile.dzn> -parser=RCPSPWetDiverse_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn19
"""

from pycsp3 import *

resources, tasks, horizon, earlinessMin, earlinessMax, tardinessMin, tardinessMax, nSolutions = data
requirements, capacities = zip(*resources)
durations, successors, deadlines = zip(*tasks)
nTasks, nResources = len(tasks), len(resources)

E, T = objectives = range(2)  # earliness and tardiness
nObjectives = len(objectives)

relevantTasks = [[i for i in range(nTasks) if requirements[r][i] > 0 and durations[i] > 0] for r in range(nResources)]

maxE = sum(deadlines[i][1] * deadlines[i][0] for i in range(nTasks))
maxT = sum(deadlines[i][2] * (horizon - deadlines[i][0]) for i in range(nTasks))

# x[k][i] is the starting time of the ith task in the kth simulation
x = VarArray(size=[nSolutions, nTasks], dom=range(horizon))

# z[j][k] is the value of the jth objective for the kth solution
z = VarArray(size=[nObjectives, nSolutions], dom=lambda i, j: range(maxE + 1) if i == 0 else range(maxT + 1))

# dmt[e][t] is 1 if the point (e,t) is dominated
dmt = VarArray(size=[earlinessMax - earlinessMin + 1, tardinessMax - tardinessMin + 1], dom={0, 1})  # range(nSolutions + 1))


def post_for(s):
    satisfy(
        # respecting precedence relations
        [s[i] + durations[i] <= s[j] for i in range(nTasks) for j in successors[i]],

        # cumulative resource constraints
        [
            Cumulative(
                tasks=[Task(origin=s[i], length=durations[i], height=requirements[r][i]) for i in relevantTasks[r]]
            ) <= capacities[r] for r in range(nResources) if sum(requirements[r][i] for i in relevantTasks[r]) > capacities[r]
        ],

        # redundant non-overlapping constraints  tag(redundant-constraints)
        [
            either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            ) for i, j in combinations(nTasks, 2) if any(requirements[r][i] + requirements[r][j] > capacities[r] for r in range(nResources))
        ]
    )


for k in range(nSolutions):
    post_for(x[k])

satisfy(
    # computing earliness values of solutions
    [z[E][j] == Sum(deadlines[i][1] * max(0, deadlines[i][0] - x[j][i]) for i in range(nTasks)) for j in range(nSolutions)],

    # computing tardiness values of solutions
    [z[T][j] == Sum(deadlines[i][2] * max(0, x[j][i] - deadlines[i][0]) for i in range(nTasks)) for j in range(nSolutions)],

    # objective values fixed for the two first solutions
    [
        z[E][0] == earlinessMin,
        z[T][0] == tardinessMax,
        z[E][1] == earlinessMax,
        z[T][1] == tardinessMin
    ],

    # computing dominated points
    [
        dmt[e][t] == disjunction(  # Exist (i.e. Count) seems more penalizing than disjunction (i.e., Intension)
            both(
                z[E][k] <= earlinessMin + e,
                z[T][k] <= tardinessMin + t
            ) for k in range(nSolutions)
        ) for e in range(earlinessMax - earlinessMin + 1) for t in range(tardinessMax - tardinessMin + 1)
    ],

    # a solution must not be dominated by any other solution
    [
        either(
            z[E][k1] < z[E][k2],
            z[T][k1] < z[T][k2]
        ) for k1 in range(nSolutions) for k2 in range(nSolutions) if k1 != k2
    ]
)

maximize(
    # maximizing the hyper-volume (the number of dominated points)
    Sum(dmt)  # [e][t] >= 1 for e in range(earlinessMax - earlinessMin + 1) for t in range(tardinessMax - tardinessMin + 1))
)

"""
1) we can post (as in Minizinc):
  a) 
  dmt = VarArray(size=[emax - emin + 1, tmax - tmin + 1], dom={0, 1})  
  dmt[e][t] == Exist((z[T, k] <= earlinessMin + e) & (z[E, k] <= tardinessMin + t) for j in range(nSolutions)) ...
  maximize(
    Sum(dmt) 
  )
 but the compilation time is higher (but more moderate with -dontuseauxcache) and introduces more aux variables 
  or 
  b)
  # dmt[e][t] is 1 if the number of solutions dominating the point (e,t)
  dmt = VarArray(size=[earlinessMax - earlinessMin + 1, tardinessMax - tardinessMin + 1], dom=range(nSolutions + 1))  # {0, 1})

  dmt[e][t] == Sum((z[T, k] <= earlinessMin + e) & (z[E, k] <= tardinessMin + t) for j in range(nSolutions)) ...
  maximize(
    Sum(dmt[e][t] >= 1 for e in range(earlinessMax - earlinessMin + 1) for t in range(tardinessMax - tardinessMin + 1))
  )
"""
