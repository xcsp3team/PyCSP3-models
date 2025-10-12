"""
Resource Availability Cost Problem (also known as Resource Investment Problem).
See EJOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2020 Minizinc challenges.
The original MZN model was proposed by Andreas Schutt - no licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  j30-13-6-1-25.json

## Model
  constraints: Cumulative, Sum

## Execution
  python RACP.py -data=<datafile.json>
  python RACP.py -data=<datafile.dzn> -parser=RACP_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S037722171730927X?via%3Dihub
  - https://www.minizinc.org/challenge/2020/results/

## Tags
  realistic, mzn18, mzn20
"""

from pycsp3 import *

horizon, resourceCosts, durations, successors, needs = data or load_json_data("j30-13-6-1-25.json")

nTasks, nResources = len(durations), len(resourceCosts)
T, R = range(nTasks), range(nResources)

lb_usage, ub_usage = [max(needs[r]) for r in R], [sum(needs[r]) for r in R]
lb_costs, ub_costs = resourceCosts * lb_usage, resourceCosts * ub_usage


def unrelated_tasks():
    succs = lambda i: successors[i] + list({v for t in [succs(j) for j in successors[i]] for v in t})  # recursive function

    all_successors = [succs(i) for i in T]
    all_predecessors = [[j for j in T if i in all_successors[j]] for i in T]
    return [[j for j in T if j not in all_successors[i] and j not in all_predecessors[i] and j != i] for i in T]


unrelated = unrelated_tasks()


def compute_ub():
    est = lambda i: 0 if len(predecessors[i]) == 0 else max(est(j) + durations[j] for j in predecessors[i])
    lct = lambda i: horizon if len(successors[i]) == 0 else min(lct(j) - durations[j] for j in successors[i])
    overlap = lambda si, di, sj, dj: si < sj + dj and sj < si + di

    predecessors = [[j for j in T if i in successors[j]] for i in T]
    es, ls = [est(i) for i in T], [lct(i) for i in T]
    rusage_es = [max(needs[r][i] + sum(needs[r][j] for j in unrelated[i] if overlap(es[i], durations[i], es[j], durations[j])) for i in T) for r in R]
    rusage_ls = [max(needs[r][i] + sum(needs[r][j] for j in unrelated[i] if overlap(ls[i] - durations[i], durations[i], ls[j] - durations[j], durations[j]))
                     for i in T) for r in R]
    return min(sum(resourceCosts[r] * rusage_es[r] for r in R), sum(resourceCosts[r] * rusage_ls[r] for r in R))


# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon + 1))

# u[r] is the usage of the rth resource
u = VarArray(size=nResources, dom=lambda r: range(lb_usage[r], ub_usage[r] + 1))

# z is the objective
z = Var(dom=range(lb_costs, min(ub_costs, compute_ub()) + 1))

satisfy(
    # ending tasks before the given horizon
    [s[i] + durations[i] <= horizon for i in T],

    # respecting precedence relations
    [s[i] + durations[i] <= s[j] for i in T for j in successors[i]],

    # redundant non-overlapping constraints   tag(redundant)
    [
        If(
            u[r] < needs[r][i] + needs[r][j],
            Then=either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            )
        ) for i in T for j in unrelated[i] for r in R if needs[r][i] + needs[r][j] > lb_usage[r]
    ],

    # redundant constraints on the lower bound of the resource capacities  tag(redundant)
    [
        u[r] - Sum(
            needs[r][j] * both(
                s[j] + durations[j] > s[i],
                s[j] <= s[i]
            ) for j in unrelated[i] if needs[r][j] > 0
        ) >= needs[r][i] for i in T for r in R if needs[r][i] > 0
    ],

    [
        Cumulative(
            origins=s,
            lengths=durations,
            heights=needs[r]
        ) <= u[r] for r in R
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
