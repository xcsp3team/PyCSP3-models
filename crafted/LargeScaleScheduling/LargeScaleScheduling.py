"""
Large scale scheduling instances have been built to show the interest of a scalable timetable filtering algorithm for the Cumulative Constraint.

## Data Example
  00100-0.json

## Model
  constraints: Cumulative, Maximum

## Execution
  python LargeScaleScheduling.py -data=<datafile.json>

## Links
  - http://becool.info.ucl.ac.be/pub/resources/large-scale-scheduling-instances.zip
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  crafted, xcsp23
"""

from pycsp3 import *

limit, durations, heights = data or load_json_data("00100-0.json")

nTasks = len(durations)
horizon = sum(durations) + 1  # trivial upper bound on the horizon

# x[i] is the starting time of the ith task
x = VarArray(size=nTasks, dom=range(horizon))

satisfy(
    # resource cumulative constraint
    Cumulative(
        origins=x,
        lengths=durations,
        heights=heights
    ) <= limit
)

minimize(
    Maximum(
        x[i] + durations[i] for i in range(nTasks)
    )
)
