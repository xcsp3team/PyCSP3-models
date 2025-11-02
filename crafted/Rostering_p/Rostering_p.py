"""
This problem was described in the JAIR paper cited below.

This problem was inspired by a rostering context.
The objective is to schedule n employees over a span of n time periods.
In each time period, n−1 tasks need to be accomplished and one employee out of the n has a break.
The tasks are fully ordered 1 to n−1; for each employee the schedule has to respect the following rules:
  - two consecutive time periods have to be assigned to either two consecutive tasks, in no matter which order i.e. (t, t+1) or (t+1, t),
    or to the same task i.e. (t, t);
- an employee can have a break after no matter which task;
- after a break an employee cannot perform the task that precedes the task prior to the break, i.e. (t, break, t−1) is not allowed.
The problem is modeled with one Regular constraint per row and one Alldifferent constraint per column.

The model/automaton below is made stricter so as (hopefully) to generate harder instances.

## Data Example
  roster-5-00-02.json

## Model
  constraints: AllDifferent, Regular

## Execution
  python Rostering_p.py -data=<datafile.json>
  python Rostering_p.py -data=<datafile.dat,10> -parser=Rostering_Parser.py

## Links
  - https://dl.acm.org/doi/abs/10.5555/2387915.2387920
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  crafted, xcsp22, xcsp25
"""

from pycsp3 import *

preset, forbidden, n = data or load_json_data("roster-5-00-02.json")


def automaton():
    # q(1,i) means before break and just after reading i
    # q(2,i) means just after reading break (0) and i before
    # q(3,i) means after break and just after reading i
    q, N = Automaton.q, range(1, n)
    t = [(q(0), 0, q(2, 0))] + [(q(2, 0), i, q(3, i)) for i in N]
    t.extend((q(0), i, q(1, i)) for i in N)
    # BE CAREFUL: rule below made stricter than Pesant's rule
    t.extend((q(1, i), j, q(1, j)) for i in N for j in (i - 1, i + 1) if 1 <= j < n)
    t.extend((q(1, i), 0, q(2, i)) for i in N)
    # BE CAREFUL: rule below made stricter than Pesant's rule
    t.extend((q(2, i), j, q(3, j)) for i in N for j in N if abs(i - j) != 1)
    # BE CAREFUL: rule below made stricter than Pesant's rule
    t.extend((q(3, i), j, q(3, j)) for i in N for j in (i - 1, i + 1) if 1 <= j < n)
    return Automaton(start=q(0), final=[q(2, i) for i in N] + [q(3, i) for i in N], transitions=t)


A = automaton()

# x[i][j] is the task (or break) performed by the ith employee at time j
x = VarArray(size=[n, n], dom=range(n))

satisfy(
    # respecting preset tasks
    [x[i][j] == k for (i, j, k) in preset],

    # respecting forbidden assignments
    [x[i][j] != k for (i, j, k) in forbidden],

    # respecting job rules for each employee
    [x[i] in A for i in range(n)],

    # all tasks are different at any time
    [AllDifferent(x[:, j]) for j in range(n)]
)

""" Comments
1) one could try:
  [x[i] in A.to_table([range(n) for _ in range(n)]) for i in range(n)]
 but tables are too large
"""
