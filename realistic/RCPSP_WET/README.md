# Problem RCPSP_WET
## Description
Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).

The objective is to find a optimal schedule so that tasks start as close as possible to
the given start time for each task, penalizing earliness or tardiness according to
the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2017 challenges.
The MZN model was proposed by University of Melbourne and NICTA (seems to be a MIT Licence).

## Data Example
  j30-27-5.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RCPSP_WET.py -data=<datafile.json>
  python RCPSP_WET.py -data=<datafile.dzn> -parser=RCPSP_WET_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn16, mzn17
