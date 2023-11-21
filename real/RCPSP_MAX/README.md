# Problem RCPSP_MAX
## Description
Resource-constrained Project Scheduling Problems with minimal and maximal time lags (RCPSP-max).
We have resources, activities, and precedence constraints.
Resources have a specific capacity and activities require some resources for their execution.
The objective is to find an optimal schedule minimizing the project duration.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010 Minizinc challenge.
The MZN model was proposed by the University of Melbourne and NICTA, Copyright (C) 2010.
The Licence seems to be like a MIT Licence.

## Data Example
  psp-c-051.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative)

## Execution
```
  python RCPSP_MAX.py -data=<datafile.json>
  python RCPSP_MAX.py -data=<datafile.dzn> -parser=RCPSP_MAX_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2010/results2010.html

## Tags
  real, mzn10
