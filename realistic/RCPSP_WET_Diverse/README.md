# Problem: RCPSP_WET_Diverse

Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).
The objective is to find an optimal schedule so that tasks start as close as possible to the given start time for each task,
penalizing earliness or tardiness according to the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The original MZN model was proposed by the University of Melbourne and NICTA - no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  j30-27-5-3.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RCPSP_WET_Diverse.py -data=<datafile.json>
  python RCPSP_WET_Diverse.py -data=<datafile.dzn> -parser=RCPSP_WET_Diverse_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn19
