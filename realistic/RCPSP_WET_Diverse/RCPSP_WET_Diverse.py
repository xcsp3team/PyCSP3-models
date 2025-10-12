"""
Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).
The objective is to find an optimal schedule so that tasks start as close as possible to the given start time for each task,
penalizing earliness or tardiness according to the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The original MZN model was proposed by the University of Melbourne and NICTA - no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  j30-27-5-3.json

## Model
  constraints: Count, Cumulative, Sum

## Execution
  python RCPSP_WET_Diverse.py -data=<datafile.json>
  python RCPSP_WET_Diverse.py -data=<datafile.dzn> -parser=RCPSP_WET_Diverse_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn19
"""

from pycsp3 import *

resources, tasks, horizon, earliness, tardiness, nSolutions = data or load_json_data("j30-27-5-3.json")

requirements, capacities = zip(*resources)
durations, successors, deadlines = zip(*tasks)

nTasks, nResources = len(tasks), len(resources)
T, S, R = range(nTasks), range(nSolutions), range(nResources)

ERL, TRD = objectives = range(2)  # earliness and tardiness
nObjectives = len(objectives)

relevantTasks = [[i for i in T if requirements[r][i] > 0 and durations[i] > 0] for r in R]

maxE = sum(deadlines[i][1] * deadlines[i][0] for i in T)
maxT = sum(deadlines[i][2] * (horizon - deadlines[i][0]) for i in T)

# x[s][i] is the starting time of the ith task in solution k
x = VarArray(size=[nSolutions, nTasks], dom=range(horizon))

# z[j][s] is the value of the jth objective for solution s
z = VarArray(size=[nObjectives, nSolutions], dom=lambda i, j: range(maxE + 1) if i == 0 else range(maxT + 1))

# dmt[e][t] is 1 if the point (e,t) is dominated
dmt = VarArray(size=[earliness.max - earliness.min + 1, tardiness.max - tardiness.min + 1], dom={0, 1})  # range(nSolutions + 1))


def post_for(s):
    satisfy(
        # respecting precedence relations
        [s[i] + durations[i] <= s[j] for i in T for j in successors[i]],

        # cumulative resource constraints
        [
            Cumulative(
                Task(
                    origin=s[i],
                    length=durations[i],
                    height=requirements[r][i]
                ) for i in relevantTasks[r]
            ) <= capacities[r] for r in R if sum(requirements[r][i] for i in relevantTasks[r]) > capacities[r]
        ],

        # redundant non-overlapping constraints  tag(redundant)
        [
            either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            ) for i, j in combinations(T, 2) if any(requirements[r][i] + requirements[r][j] > capacities[r] for r in R)
        ]
    )


for k in range(nSolutions):
    post_for(x[k])

satisfy(
    # computing earliness values of solutions
    [z[ERL][s] == Sum(deadlines[i][1] * max(0, deadlines[i][0] - x[s][i]) for i in T) for s in S],

    # computing tardiness values of solutions
    [z[TRD][s] == Sum(deadlines[i][2] * max(0, x[s][i] - deadlines[i][0]) for i in T) for s in S],

    # objective values fixed for the two first solutions
    [
        z[ERL][0] == earliness.min,
        z[TRD][0] == tardiness.max,
        z[ERL][1] == earliness.max,
        z[TRD][1] == tardiness.min
    ],

    # computing dominated points
    [
        dmt[e][t] == disjunction(  # Exist (i.e. Count) seems more penalizing than disjunction (i.e., Intension)
            both(
                z[ERL][s] <= earliness.min + e,
                z[TRD][s] <= tardiness.min + t
            ) for s in S
        ) for e in range(earliness.max - earliness.min + 1) for t in range(tardiness.max - tardiness.min + 1)
    ],

    # a solution must not be dominated by any other solution
    [
        either(
            z[ERL][s1] < z[ERL][s2],
            z[TRD][s1] < z[TRD][s2]
        ) for s1 in S for s2 in S if s1 != s2
    ]
)

maximize(
    # maximizing the hyper-volume (the number of dominated points)
    Sum(dmt)
)

"""
1) We can post (as in Minizinc):
  a) 
  dmt = VarArray(size=[emax - emin + 1, tmax - tmin + 1], dom={0, 1})  
  dmt[e][t] == Exist((z[T, k] <= earlinessMin + e) & (z[E, k] <= tardinessMin + t) for j in range(nSolutions)) ...
  maximize(
    Sum(dmt) 
  )
 but the compilation time is higher (but more moderate with -dont_use_aux_cache) and introduces more aux variables 
  or 
  b)
  # dmt[e][t] is 1 if the number of solutions dominating the point (e,t)
  dmt = VarArray(size=[earlinessMax - earlinessMin + 1, tardinessMax - tardinessMin + 1], dom=range(nSolutions + 1))  # {0, 1})

  dmt[e][t] == Sum((z[T, k] <= earlinessMin + e) & (z[E, k] <= tardinessMin + t) for j in range(nSolutions)) ...
  maximize(
    Sum(dmt[e][t] >= 1 for e in range(earlinessMax - earlinessMin + 1) for t in range(tardinessMax - tardinessMin + 1))
  )
"""
