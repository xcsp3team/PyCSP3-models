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
  - https://www.minizinc.org/challenge/2021/results/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn21, mzn25
"""

from pycsp3 import *

setup_times, maxColors, cyclesPerJob, nJobs, nColors, nLines, compatibilities, programs, moulds, demands = data

slots, cycle_time = [list(t) for t in zip(*programs)]  # we need lists to be able to insert a new value (0)
dqty, ddue, dcol, dmld = zip(*demands)
nPrograms, nMoulds, nDemands = len(programs), len(moulds), len(demands)

J, M, C, D = range(nJobs), range(nMoulds), range(nColors), range(nDemands)

slots0 = cp_array([0] + slots)
cycle_time0 = cp_array([0] + cycle_time)
maxMoulds = max(slots)  # per job

demandedColors = [[c for c in C if any(color == c + 1 and mould == m + 1 for (_, _, color, mould) in demands)] for m in M]
compatibleDemands = [[d2 for d2 in D if ddue[d2] <= ddue[d] and dmld[d2] == dmld[d] and dcol[d2] == dcol[d]] for d in D]

lb, ub = min(cycle_time) * cyclesPerJob.min, nJobs * cyclesPerJob.max * max(cycle_time) + nJobs * setup_times.program
timeline = range(lb, ub + 1)

# jp[j] is the program assigned to job j
jp = VarArray(size=nJobs, dom=range(nPrograms + 1))

# jl[j] is the length (number of cycles) of job j
jl = VarArray(size=nJobs, dom=range(cyclesPerJob.min, cyclesPerJob.max + 1))

# jm[j][m][c] is the number of moulds of type m with color c assigned to job j
jm = VarArray(size=[nJobs, nMoulds, nColors], dom=range(maxMoulds + 1))

# jmp[j][m][c] is the total number of moulds of type m with color c produced by job j
jmp = VarArray(size=[nJobs, nMoulds, nColors], dom=range(maxMoulds * cyclesPerJob.max + 1))

# je[j] is the finishing time (end) of job j
je = VarArray(size=nJobs, dom=timeline)

# jt[j] is the processing time of job j
jt = VarArray(size=nJobs, dom=range(cyclesPerJob.max * max(cycle_time) + 1))

# de[i] is finishing time (end) of the ith demand
de = VarArray(size=nDemands, dom=timeline)

# dj[i] is the finishing job for the ith demand
dfj = VarArray(size=nDemands, dom=range(nJobs))

# the make-span of the schedule
mks = Var(dom=timeline)

# the waste (number of produced moulds that are not consumed)
wst = Var(dom=range(maxMoulds * cyclesPerJob.max * nJobs))

# the tardiness of all demands
trd = Var(dom=range(sum(max(0, ub - ddue[d]) for d in D)))

satisfy(
    # breaking symmetries  tag(symmetry-breaking)
    [
        If(
            jp[j] == 0,
            Then=[
                jp[j + 1] == 0 if j < nJobs - 1 else None,
                jl[j] == cyclesPerJob.min
            ]
        ) for j in J
    ],

    # checking number of assigned moulds per job
    [
        Sum(jm[j]) == slots0[jp[j]] for j in J
    ],

    # checking number of available moulds per type
    [
        Sum(jm[j][m]) <= moulds[m].available for j in J for m in M
    ],

    # checking the number of colors and lines per job
    [
        Sum(
            jm[j][m][c] > 0 for m in M if moulds[m].line in range(1, nLines + 1) for c in C
        ) <= maxColors for j in J
    ],

    # checking that demands are fulfilled
    [
        Sum(
            jmp[:, m, c]
        ) >= sum(quantity for (quantity, _, color, mould) in demands if mould == m + 1 and color == c + 1)
        for m in M for c in demandedColors[m]
    ],

    # enforcing that moulds are compatible with programs
    [
        If(
            jp[j] != moulds[m].program,
            Then=Sum(jm[j][m]) == 0
        ) for j in J for m in M
    ],

    # checking color compatibility
    [
        If(
            Sum(jm[j, :, c1]) > 0,
            Then=Sum(jm[j, :, c2]) == 0
        ) for j in J for c1, c2 in combinations(C, 2) if compatibilities[c1][c2] == 0
    ],

    # computing produced job moulds
    [
        jmp[j][m][c] == jm[j][m][c] * jl[j] for j in J for m in M for c in C
    ],

    # setting job times
    [
        If(
            jp[j] == p,
            Then=jt[j] == jl[j] * cycle_time0[p]
        ) for j in J for p in range(1, nPrograms + 1)
    ],

    # setting job end times
    (
        If(
            jp[j] > 0,
            Then=je[j] == jt[0] + Sum(
                jt[k] + setup_times.sequence + (jp[k - 1] != jp[k]) * (setup_times.program - setup_times.sequence) for k in range(1, j + 1)
            ), Else=je[j] == lb
        ) for j in J
    ),

    # setting demand end times
    (
        (
            de[d] == je[dfj[d]],
            Sum(jmp[i][dmld[d] - 1][dcol[d] - 1] * (i <= dfj[d]) for i in J) >= K,
            Sum(jmp[i][dmld[d] - 1][dcol[d] - 1] * (i < dfj[d]) for i in J) < K,
            jp[dfj[d]] > 0
        ) for d in D if [K := sum(dqty[d2] for d2 in compatibleDemands[d])]
    ),

    # computing objective components
    [
        mks == Maximum(je),
        wst == Sum(jmp) - sum(dqty),
        trd == Sum((de[d] > ddue[d]) * (de[d] - ddue[d]) for d in D)
    ]
)

minimize(
    mks + trd + wst
)

""" Comments
1) One could write:
   [If(jp[j] == 0, Then=jp[j + 1] == 0) for j in range(nJobs - 1)],
   [If(jp[j] == 0, Then=jl[j] == yclesPerJob.min) for j in range(nJobs)]
  for symmetry breaking

2) Don't use (K := sum(dqty[d2] for d2 in compatibleDemands[d])) because it may be o and bool((0)) is False.
 instead, use [K := sum(dqty[d2] for d2 in compatibleDemands[d])]
"""

# jm[i][k][l] > 0 for m in range(nLines) for k in range(nMoulds) if moulds[k].line == m + 1 for l in range(nColors)


# [If(jp[i] > 0, Then=je[i] == jt[0] + Sum(jt[k] + seq_setup + (jp[k - 1] != jp[k]) * (pro_setup - seq_setup) for k in range(1, i + 1)))
#  for i in range(nJobs)],
# [If(jp[i] == 0, Then=je[i] == lb) for i in range(nJobs)]
