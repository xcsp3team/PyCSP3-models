"""
Artificial Teeth Scheduling Problem.
See ICAPS paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The MZN model was proposed by Felix Winter, with a Licence that seems to be like the MIT Licence.
Accompanying instances are based on real-life instances.

## Data Example
  05-0p15.json

## Model
  constraints: Maximum, Sum

## Execution
  python ATSP.py -data=<datafile.json>
  python ATSP.py -data=<datafile.dzn> -parser=ATSP_ParserZ.py

## Links
  - https://ojs.aaai.org/index.php/ICAPS/article/view/15997W
  - https://dbai.tuwien.ac.at/staff/winter/
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn21
"""

from pycsp3 import *

pro_setup, seq_setup, maxColors, minCycles, maxCycles, nJobs, nColors, nLines, compatibilities, programs, moulds, demands = data

slots, cycle_time = [list(t) for t in zip(*programs)]  # we need lists to be able to insert a new value (0)
dqty, ddue, dcol, dmld = zip(*demands)
nPrograms, nMoulds, nDemands = len(programs), len(moulds), len(demands)

slots0 = cp_array([0] + slots)
cycle_time0 = cp_array([0] + cycle_time)
maxMoulds = max(slots)  # per job

demandedColors = [[c for c in range(nColors) if any(color == c + 1 and mould == m + 1 for (_, _, color, mould) in demands)] for m in range(nMoulds)]
compatibleDemands = [[d2 for d2 in range(nDemands) if ddue[d2] <= ddue[d] and dmld[d2] == dmld[d] and dcol[d2] == dcol[d]] for d in range(nDemands)]

lb, ub = min(cycle_time) * minCycles, nJobs * maxCycles * max(cycle_time) + nJobs * pro_setup
timeline = range(lb, ub + 1)

# jp[i] is the program assigned to the ith job
jp = VarArray(size=nJobs, dom=range(nPrograms + 1))

# jl[i] is the length (number of cycles) of the ith job
jl = VarArray(size=nJobs, dom=range(minCycles, maxCycles + 1))

# jm[i][k][j] is the number of moulds of the kth type with the jth color assigned to the ith job
jm = VarArray(size=[nJobs, nMoulds, nColors], dom=range(maxMoulds + 1))

# jmp[i][k][j] is the total number of moulds of the kth type with the jth color produced by the ith job
jmp = VarArray(size=[nJobs, nMoulds, nColors], dom=range(maxMoulds * maxCycles + 1))

# je[i] is the finishing time (end) of the ith job
je = VarArray(size=nJobs, dom=timeline)

# jt[i] is the processing time of the ith job
jt = VarArray(size=nJobs, dom=range(maxCycles * max(cycle_time) + 1))

# de[i] is finishing time (end) of the ith demand
de = VarArray(size=nDemands, dom=timeline)

# dj[i] is the finishing job for the ith demand
dfj = VarArray(size=nDemands, dom=range(nJobs))

# the make-span of the schedule
makespan = Var(dom=timeline)

# the waste (number of produced moulds that are not consumed)
waste = Var(dom=range(maxMoulds * maxCycles * nJobs))

# the tardiness of all demands
tardiness = Var(dom=range(sum(max(0, ub - ddue[d]) for d in range(nDemands))))

satisfy(
    # breaking symmetries  tag(symmetry-breaking)
    [
        If(
            jp[i] == 0,
            Then=[
                jp[i + 1] == 0 if i < nJobs - 1 else None,
                jl[i] == minCycles
            ]
        ) for i in range(nJobs)
    ],

    # checking number of assigned moulds per job
    [
        Sum(jm[i]) == slots0[jp[i]] for i in range(nJobs)
    ],

    # checking number of available moulds per type
    [
        Sum(jm[i][k]) <= moulds[k].available for i in range(nJobs) for k in range(nMoulds)
    ],

    # checking the number of colors and lines per job
    [
        Sum(
            jm[i][k][l] > 0 for k in range(nMoulds) if moulds[k].line in range(1, nLines + 1) for l in range(nColors)
        ) <= maxColors
        for i in range(nJobs)
    ],

    # checking that demands are fulfilled
    [
        Sum(
            jmp[:, m, c]
        ) >= sum(quantity for (quantity, _, color, mould) in demands if mould == m + 1 and color == c + 1)
        for m in range(nMoulds) for c in demandedColors[m]
    ],

    # enforcing that moulds are compatible with programs
    [
        If(
            jp[i] != moulds[k].program,
            Then=Sum(jm[i][k]) == 0
        ) for i in range(nJobs) for k in range(nMoulds)
    ],

    # checking color compatibility
    [
        If(
            Sum(jm[i, :, c1]) > 0,
            Then=Sum(jm[i, :, c2]) == 0
        ) for i in range(nJobs) for c1, c2 in combinations(nColors, 2) if compatibilities[c1][c2] == 0
    ],

    # computing produced job moulds
    [
        jmp[i][k][j] == jm[i][k][j] * jl[i] for i in range(nJobs) for k in range(nMoulds) for j in range(nColors)
    ],

    # setting job times
    [
        If(
            jp[i] == p,
            Then=jt[i] == jl[i] * cycle_time0[p]
        ) for i in range(nJobs) for p in range(1, nPrograms + 1)
    ],

    # setting job end times
    (
        If(
            jp[i] > 0,
            Then=je[i] == jt[0] + Sum(jt[k] + seq_setup + (jp[k - 1] != jp[k]) * (pro_setup - seq_setup) for k in range(1, i + 1)),
            Else=je[i] == lb
        ) for i in range(nJobs)
    ),

    # setting demand end times
    (
        (
            de[d] == je[dfj[d]],
            Sum(jmp[i][dmld[d] - 1][dcol[d] - 1] * (i <= dfj[d]) for i in range(nJobs)) >= K,
            Sum(jmp[i][dmld[d] - 1][dcol[d] - 1] * (i < dfj[d]) for i in range(nJobs)) < K,
            jp[dfj[d]] > 0
        ) for d in range(nDemands) if [K := sum(dqty[d2] for d2 in compatibleDemands[d])]
    ),

    # computing objective components
    [
        makespan == Maximum(je),
        Sum(jmp) - waste == sum(dqty),
        tardiness == Sum((de[d] > ddue[d]) * (de[d] - ddue[d]) for d in range(nDemands))
    ]
)

minimize(
    makespan + tardiness + waste
)

"""
1)  waste == Sum(jmp) - sum(dqty) compiles badly (how to recognize a possible Sum?)
2) one could write:
   [If(jp[i] == 0, Then=jp[i + 1] == 0) for i in range(nJobs - 1)],
   [If(jp[i] == 0, Then=jl[i] == minCycles) for i in range(nJobs)]
  for symmetry breaking
3) don't use (K := sum(dqty[d2] for d2 in compatibleDemands[d])) because it may be o and bool((0)) is False.
 instead, use [K := sum(dqty[d2] for d2 in compatibleDemands[d])]
"""

# jm[i][k][l] > 0 for m in range(nLines) for k in range(nMoulds) if moulds[k].line == m + 1 for l in range(nColors)


# [If(jp[i] > 0, Then=je[i] == jt[0] + Sum(jt[k] + seq_setup + (jp[k - 1] != jp[k]) * (pro_setup - seq_setup) for k in range(1, i + 1)))
#  for i in range(nJobs)],
# [If(jp[i] == 0, Then=je[i] == lb) for i in range(nJobs)]
