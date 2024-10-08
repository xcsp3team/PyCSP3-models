"""
Resource Availability Cost Problem (also known as Resource Investment Problem).
See EJOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2020 Minizinc challenges.
The MZN model was proposed by Andreas Schutt.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  j30-13-6-1-25.json

## Model
  constraints: Cumulative, Sum

## Execution
  python RACP.py -data=<datafile.json>
  python RACP.py -data=<datafile.dzn> -parser=RACP_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S037722171730927X?via%3Dihub
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn18, mzn20
"""

from pycsp3 import *

horizon, resourceCosts, durations, successors, needs = data
nResources, nTasks = len(resourceCosts), len(durations)

lb_usage, ub_usage = [max(needs[r]) for r in range(nResources)], [sum(needs[r]) for r in range(nResources)]
lb_costs, ub_costs = resourceCosts * lb_usage, resourceCosts * ub_usage


def unrelated_tasks():
    succs = lambda i: successors[i] + list({v for t in [succs(j) for j in successors[i]] for v in t})

    all_successors = [succs(i) for i in range(nTasks)]
    all_predecessors = [[j for j in range(nTasks) if i in all_successors[j]] for i in range(nTasks)]
    return [[j for j in range(nTasks) if j not in all_successors[i] and j not in all_predecessors[i] and j != i] for i in range(nTasks)]


unrelated = unrelated_tasks()


def compute_ub():
    est = lambda i: 0 if len(predecessors[i]) == 0 else max(est(j) + durations[j] for j in predecessors[i])
    lct = lambda i: horizon if len(successors[i]) == 0 else min(lct(j) - durations[j] for j in successors[i])
    overlap = lambda si, di, sj, dj: si < sj + dj and sj < si + di

    predecessors = [[j for j in range(nTasks) if i in successors[j]] for i in range(nTasks)]
    es, ls = [est(i) for i in range(nTasks)], [lct(i) for i in range(nTasks)]
    rusage_es = [max(needs[r][i] + sum(needs[r][j] for j in unrelated[i] if overlap(es[i], durations[i], es[j], durations[j]))
                     for i in range(nTasks)) for r in range(nResources)]
    rusage_ls = [max(needs[r][i] + sum(needs[r][j] for j in unrelated[i] if overlap(ls[i] - durations[i], durations[i], ls[j] - durations[j], durations[j]))
                     for i in range(nTasks)) for r in range(nResources)]
    return min(sum(resourceCosts[r] * rusage_es[r] for r in range(nResources)), sum(resourceCosts[r] * rusage_ls[r] for r in range(nResources)))


# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon + 1))

# u[r] is the usage of the rth resource
u = VarArray(size=nResources, dom=lambda r: range(lb_usage[r], ub_usage[r] + 1))

# z is the objective
z = Var(dom=range(lb_costs, min(ub_costs, compute_ub()) + 1))

satisfy(
    # ending tasks before the given horizon
    [s[i] + durations[i] <= horizon for i in range(nTasks)],

    # respecting precedence relations
    [s[i] + durations[i] <= s[j] for i in range(nTasks) for j in successors[i]],

    # redundant non-overlapping constraints   tag(redundant)
    [
        If(
            u[r] < needs[r][i] + needs[r][j],
            Then=either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            )
        ) for i in range(nTasks) for j in unrelated[i] for r in range(nResources) if needs[r][i] + needs[r][j] > lb_usage[r]
    ],

    # redundant constraints on the lower bound of the resource capacities  tag(redundant)
    [
        u[r] - Sum(
            needs[r][j] * both(
                s[j] + durations[j] > s[i],
                s[j] <= s[i]
            ) for j in unrelated[i] if needs[r][j] > 0
        ) >= needs[r][i] for i in range(nTasks) for r in range(nResources) if needs[r][i] > 0
    ],

    [
        Cumulative(
            origins=s,
            lengths=durations,
            heights=needs[r]
        ) <= u[r] for r in range(nResources)
    ],

    # computing the value of the objective
    z == resourceCosts * u
)

minimize(
    z
)

""" Comments
1) Note that:
 z == resourceCosts * u
   is equivalent to: 
 z == Sum(resourceCosts[r] * u[r] for r in range(nResources))
"""
