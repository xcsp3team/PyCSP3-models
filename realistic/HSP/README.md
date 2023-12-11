# Problem HSP
## Description
We consider a facility with a single handling resource (a hoist).
The hoist has to perform a sequence of moves in order to accomplish a set of jobs, with varying
processing requirements, while satisfying processing and transport resource constraints.
The objective is to determine a feasible schedule (i.e., a sequence) that minimizes the total processing
time of a set of jobs (i.e., the makespan), while, at the same time, satisfying surface treatment constraints

## Data (example)
  10405.json

## Model
  Three variants compute differently dip durations:
  - a main variant involving logical constraints
  - a variant 'aux' involving auxiliary variables and logical constraints
  - a variant 'table' involving auxiliary variables and table constraints

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python HSP.py -data=<datafile.json>
  - python HSP.py -data=<datafile.json> -variant=aux
  - python HSP.py -data=<datafile.json> -variant=table

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054815002373
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
