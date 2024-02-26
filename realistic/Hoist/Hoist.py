"""
Hoist Scheduling (M hoists, 1 track).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by M. Wallace and N. Yorke-Smith,
and released under CC BY-NC-SA license (https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Data Example
  PU-1-2-2.json

## Model
  constraints: Sum

## Execution
  python Hoist.py -data=<datafile.json>
  python Hoist.py -data=<datafile.dzn> -parser=Hoist_ParserZ.py

## Links
  - https://data.4tu.nl/articles/_/12682700/1
  - https://link.springer.com/article/10.1007/s10601-020-09316-z
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

limitJobs, minTimes, maxTimes, eTimes, fTimes, multiplier, nHoists, capacity = data
nTanks = len(minTimes)
N = multiplier * nTanks

multtank = [((i - 1) % nTanks) + 1 for i in range(N + 2)]
tmin = [minTimes[multtank[i] - 1] for i in range(N + 2)]  # minimum time for job in each tank
tmax = [maxTimes[multtank[i] - 1] for i in range(N + 2)]  # maximum time for job in each tank


def e(i, j):
    ic = nTanks + 1 if i == N + 1 else multtank[i]
    jc = 0 if j == 0 else multtank[j]
    cycle_i = multiplier - 1 if i == N + 1 else (i - 1) // nTanks
    cycle_j = 0 if j == 0 else (j - 1) // nTanks
    return 5 * abs(cycle_i - cycle_j) + eTimes[ic - 1, jc]


def f(i):
    return fTimes[0 if i == 0 else multtank[i]]


period_lb = sum(f(k) + min([0 if k == N else tmin[k + 1]] + [e(k + 1, j) for j in range(N + 1) if j != k + 1]) for k in range(1, N + 1)) // nHoists
period_ub = sum(list(reversed(sorted([tmin[k] + f(k) for k in range(1, N + 1)])))[p - 1] for p in range(1, N // nHoists + 1))

# r[i] is the removal time upon completion of the ith treatment
r = VarArray(size=N + 1, dom=range(period_ub + 1))

# h[i] is the hoist performing the ith treatment
h = VarArray(size=N + 1, dom=range(nHoists))

# b[i] is the number of jobs in the ith tank at the end of the cycle
b = VarArray(size=N, dom=range(capacity + 1))

# z is the cycle length (period)
z = Var(dom=range(period_lb, period_ub + 1))

satisfy(
    # constraining removal times and period
    [
        r[0] == 0,
        r[N] + f(N) <= z,
        [r[i] <= z for i in range(1, N + 1)]
    ],

    # respecting the maximum number of jobs under treatment in a single cycle
    Sum(b) <= limitJobs,

    # enforcing minimum and maximum soak times in each tank
    [
        (
            r[i] + z * b[i - 1] >= r[i - 1] + f(i - 1) + tmin[i],
            r[i] + z * b[i - 1] <= r[i - 1] + f(i - 1) + tmax[i]
        ) for i in range(1, N + 1)
    ],

    # tag(symmetry-breaking)
    h[0] == 0,

    # (1) and (2)
    [
        If(
            h[i] <= h[j],  # in case higher numbered hoist removes from lower number tank
            Then=[
                either(  # (1) ensure the times are not overlapping
                    r[i] + f(i) + e(i + 1, j) <= r[j],
                    r[j] + f(j) + e(j + 1, i) <= r[i]
                ),
                both(  # (2) ensure it concludes before the next action
                    r[i] + f(i) + e(i + 1, j) <= r[j] + z,
                    r[j] + f(j) + e(j + 1, i) <= r[i] + z
                )
            ]
        ) for i in range(1, N + 1) for j in range(i)
    ],

    # (3) hoists at same tank: add delays while hoists go up and down
    [r[i] <= r[i - 1] + f(i - 1) + period_ub * (capacity - b[i - 1]) for i in range(1, N + 1)]
)

minimize(
    # minimizing the period
    z
)
