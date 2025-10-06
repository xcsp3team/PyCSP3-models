"""
A staff member must be assigned to each "day" in a rostering period.
A "day", means either one of Monday through to Thursday or all of Friday through Sunday; the latter is considered to be the weekend.
Individual staff members
  - may be unavailable on some days and may also be required to be on-call on some (other) days,
  - should ideally work the same number of week days and weekends over the rostering period,
  - should not be on-call for more than two days in a row (unless fixed in advance) and prefer not be on-call consecutive days in a row,
  - who are on-call over the weekend prefer not be on-call on the Wednesday before that weekend.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2018 Minizinc challenges.
The original MZN model was proposed by Julien Fischer -- no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  04s-010d.json

## Model
  constraints: Cardinality, Sum

## Execution
  python OncallRostering.py -data=<datafile.json>
  python OncallRostering.py -data=<datafile.dzn> -parser=OncallRostering_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2018/results/

## Tags
  realistic, mzn13, mzn18
"""

from pycsp3 import *

nDays, workers, offset, costs = data or load_json_data("04s-010d.json")

workloads, unavailableDays, fixedDays = zip(*workers)
nWorkers = len(workers)

assert nDays > 5 and nWorkers > 1
all_fixed = {v for t in fixedDays for v in t}
weekends = [i for i in range(nDays) if i % 5 == offset]
nWeekends = len(weekends)

# x[i] is the worker for the ith day
x = VarArray(size=nDays, dom=range(nWorkers))

# do[j] is the number of times the jth worker is set for a regular day of the week
do = VarArray(size=nWorkers, dom=range(nDays - nWeekends + 1))

# wo[j] is the number of times the jth worker is set for a weekend
wo = VarArray(size=nWorkers, dom=range(nWeekends + 1))

# db is the balance violation wrt working days
db = Var(dom=range(nDays + 1))

# db is the balance violation wrt working weekends
wb = Var(dom=range(nDays + 1))

satisfy(
    # respecting fixed working days
    [
        x[i] == j
        for j in range(nWorkers) for i in fixedDays[j]
    ],

    # respecting unavailability of workers
    [
        x[i] != j
        for j in range(nWorkers) for i in unavailableDays[j]
    ],

    # counting working (regular) days by each worker
    Cardinality(
        within=[x[i] for i in range(nDays) if i not in weekends],
        occurrences=do
    ),

    # counting working weekends by each worker
    Cardinality(
        within=x[weekends],
        occurrences=wo
    ),

    # computing the balance violation wrt working days
    [
        abs(workloads[j2] * do[j1] - workloads[j1] * do[j2]) <= 100 * db
        for j1, j2 in combinations(nWorkers, 2)
    ],

    # computing the balance violation wrt working weekends
    [
        abs(workloads[j2] * wo[j1] - workloads[j1] * wo[j2]) <= 100 * wb
        for j1, j2 in combinations(nWorkers, 2)
    ],

    # no three successive days by the same worker (except if fixed days)
    [
        If(
            x[i] == x[i + 1],
            Then=x[i] != x[i + 2]
        ) for i in range(nDays - 2) if not {i, i + 1, i + 2}.issubset(all_fixed)
    ],

    # no two successive weekends by the same worker (except if fixed days)
    [
        x[i] != x[i + 5]
        for i in weekends if i + 5 < nDays and not {i, i + 5}.issubset(all_fixed)
    ],

    # a worker is not set for the day after the first one in case it is a weekend (except if fixed days)
    x[0] != x[1] if 0 in weekends and not {0, 1}.issubset(all_fixed) else None,

    # a worker is not set for the day before the last one in case it is a weekend (except if fixed days)
    x[nDays - 1] != x[nDays - 2] if nDays - 1 in weekends and not {nDays - 1, nDays - 2}.issubset(all_fixed) else None,

    # a worker is not set for the day before and after any day in case it is a weekend (except if fixed days)
    [
        x[i] != x[i + g]
        for i in weekends if 0 < i < nDays - 1 and not {i - 1, i, i + 1}.issubset(all_fixed) for g in (-1, 1)
    ]
)

minimize(
    Sum((x[i] == x[i + 1]) * costs.adjacency for i in range(nDays - 2))
    + Sum((x[i] == x[i - 2]) * costs.wednesday for i in weekends if i >= 2)
    + db + wb
)

""" Comments
1) Note that: 
   - nDays-2 is used instead of nDays- 1 when considering adjacency cost (seems to be a typo in the mzn model? we keep it for reproducing results))
   - instead of explicitly introducing auxiliary variables to deal with some penalties (costs), 
     we post everything inside the objective function
2) Note that:
  x[weekends] 
 is equivalent to:
  [x[i] for i in weekends]
3) For the last statement ending with 'else None', one could alternatively write:
    # a worker is not set for the day before the last one in case it is a weekend (except if fixed days)
    If(
      nDays - 1 in weekends and not {nDays - 1, nDays - 2}.issubset(all_fixed),
      Then=x[nDays - 1] != x[nDays - 2]
    ),
  but this use of If with a condition that is not constraint-based (i.e. not involving a variable of the model) may look not appropriate
  or we could simply write (after having closed the first call to satisfy()
    if nDays - 1 in weekends and not {nDays - 1, nDays - 2}.issubset(all_fixed):
        satisfy(
             # a worker is not set for the day before the last one in case it is a weekend (except if fixed days)
             x[nDays - 1] != x[nDays - 2]
        )   
"""
