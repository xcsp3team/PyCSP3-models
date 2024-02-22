"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  2w-1.json

## Model
  constraints: Count, Sum

## Execution
  python SkillAllocation.py -data=<datafile.json>
  python SkillAllocation.py -data=<datafile.dzn> -parser=SkillAllocation_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

nTrainings, nMaxJobs, engineerSkills, engineerLocations, jobs = data
nEngineers, nSkills, nJobs, nOverseasCap = len(engineerSkills), len(engineerSkills[0]), len(jobs), 5

qualifiedEngineers = [[e for e in range(nEngineers) if engineerSkills[e][job[0]] == 1] for job in jobs]

# x[i] is the engineer assigned to the ith job
x = VarArray(size=nJobs, dom=range(nEngineers))

# y[e][k] is the new skill (or -1) obtained by the kth training for the engineer e
y = VarArray(size=[nEngineers, nTrainings], dom=range(-1, nSkills))

satisfy(
    # computing new skills
    [y[e][t] in {-1}.union(s for s in range(nSkills) if engineerSkills[e][s] == 0) for e in range(nEngineers) for t in range(nTrainings)],

    # not exceeding the maximum number of jobs per engineer
    [Sum(x[i] == e for i in range(nJobs)) <= nMaxJobs for e in range(nEngineers)],

    # not exceeding the maximum number of oversea jobs per engineer
    [Sum(x[i] == e for i in range(nJobs) if jobs[i][4] == 1) <= nOverseasCap for e in range(nEngineers)],

    # ensuring that a qualified engineer is assigned to each job
    [
        If(
            x[i] not in qualifiedEngineers[i],
            Then=Exist(
                both(
                    y[e][t] == jobs[i][0],
                    x[i] == e
                ) for e in range(nEngineers) for t in range(nTrainings)
            )
        ) for i in range(nJobs)
    ]
)

minimize(
    # minimizing the number of new skills
    Sum(y[e][t] >= 0 for e in range(nEngineers) for t in range(nTrainings))
)
