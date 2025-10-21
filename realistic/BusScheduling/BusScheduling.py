"""
Problem 022 of csplib.

Bus driver scheduling can be formulated as a set partitioning problem.
These consist of a given set of tasks (pieces of work) to cover and a large set of possible shifts, where each shift covers a subset of the tasks
and has an associated cost. We must select a subset of possible shifts that covers each piece of work once and only once: this is called a partition.

## Data Illustration
  t1.json

## Model
  constraints: Sum, Count

## Execution
  python BusScheduling.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob022/
 - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, csplib, xcsp25
"""

from pycsp3 import *

nTasks, shifts = data or load_json_data("t1.json")

nShifts = len(shifts)

# x[i] is 1 iff the ith shift is selected
x = VarArray(size=nShifts, dom={0, 1})

satisfy(
    # each task is covered by exactly one shift
    ExactlyOne(x[i] for i, shift in enumerate(shifts) if t in shift) for t in range(nTasks)
)

minimize(
    # minimizing the number of shifts
    Sum(x)
)

""" Comments
1) Note that the default value for Count/ExactlyOne is 1. We can equivalently write:
 Count([x[i] for i, shift in enumerate(shifts) if t in shift], value=1) == 1 for t in range(nTasks)
"""
