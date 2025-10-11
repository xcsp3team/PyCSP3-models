"""
The Resource Investment Problem (RIP) is also known as the Resource Availability Cost Problem (RACP).
The RIP assumes that the level of renewable resources can be varied at a certain cost and aims at minimizing this total cost
of the (unlimited) renewable resources required to complete the project by a pre-specified project deadline.


## Data Example
  25-0-j060-01-01.json

## Model
  constraints: Cumulative, Sum

## Execution
  python RIP.py -data=<datafile.json>
  python RIP.py -data=<datafile.txt> -parser=RIP_Parser.py

## Links
  - https://www.projectmanagement.ugent.be/research/project_scheduling/racp
  - https://ideas.repec.org/a/eee/ejores/v266y2018i2p472-486.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

horizon, costs, tasks = data or load_json_data("25-0-j060-01-01.json")

durations, successors, requirements = zip(*tasks)
nResources, nTasks = len(costs), len(tasks)
requirements = [[r[k] for r in requirements] for k in range(nResources)]

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon + 1))

# u[k] is the maximal usage (at any time) of the kth resource
u = VarArray(size=nResources, dom=lambda k: range(max(requirements[k]), sum(requirements[k]) + 1))

satisfy(
    # ending tasks before the given horizon
    [s[i] + durations[i] <= horizon for i in range(nTasks)],

    # respecting precedence relations
    [s[i] + durations[i] <= s[j] for i in range(nTasks) for j in successors[i]],

    # cumulative resource constraints
    [
        Cumulative(
            origins=s,
            lengths=durations,
            heights=requirements[k]
        ) <= u[k] for k in range(nResources)
    ]
)

minimize(
    # minimizing weighted usage of resources
    costs * u
)

""" Comments
1) costs * u
   is a shortcut for 
 Sum(costs[r] * u[r] for r in range(nResources))
"""
