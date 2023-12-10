"""
Problem 022 of csplib.<br />
Bus driver scheduling can be formulated as a set paritioning problem. These consist of a given set of tasks (pieces of work) to cover and a large set of possible shifts, where each shift covers a subset of the tasks and has an associated cost. We must select a subset of possible shifts that covers each piece of work once and only once: this is called a partition.

## Data

TODO

## Model
constraints: Sum, Count

## Command Line
python BusScheduling.py -data=BusScheduling_example.dzn

## Links
 - https://www.csplib.org/Problems/prob022/

## Tags
  recreational, csplib
"""

from pycsp3 import *

nTasks, shifts = data
nShifts = len(shifts)

# x[i] is 1 iff the ith shift is selected
x = VarArray(size=nShifts, dom={0, 1})

satisfy(
    # each task is covered by exactly one shift
    Count(x[i] for i, shift in enumerate(shifts) if t in shift) == 1 for t in range(nTasks)
)

minimize(
    # minimizing the number of shifts
    Sum(x)
)

""" Comments
1) Note that the default value for Count is 1. We can equivalently write:
 Count([x[i] for i, shift in enumerate(shifts) if t in shift], value=1) == 1 for t in range(nTasks)
"""
