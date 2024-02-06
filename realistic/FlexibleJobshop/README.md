# Problem FlexibleJobshop

Flexible Job Shop Scheduling is more general than Job Shop Scheduling as some tasks can be run an alternative machines.
The goal remains to find a feasible schedule minimising the makespan.
Each job is composed of tasks and each task must be executed by exactly one among several optional operations.
Machines and durations are given for optional operations.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013 Minizinc challenge.
The MZN model was proposed by Andreas Schutt (Copyright 2013 National ICT Australia).

## Data Example
  easy01.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python FlexibleJobshop.py -data=<datafile.json>
  python FlexibleJobshop.py -data=<datafile.dzn> -parser=FlexibleJobshop_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  realistic, mzn13
