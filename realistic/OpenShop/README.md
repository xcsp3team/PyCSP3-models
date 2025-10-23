# Problem: OpenShop

An open shop problem is identical to a job-shop problem with the exception that there is no ordering on the tasks of a job.
A job is a sequence of tasks.
A task involves processing by a single machine for some duration.
A machine can operate on at most one task at a time, for each job at most one task can be performed at a time.
Tasks cannot be interrupted.
The goal is to schedule each job to minimise the finishing time (makespan).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
The original MZN model was proposed by Diarmuid Grimes (adapted from Ralph Becket model).
Instances were taken from benchmarks proposed by Taillard, Gueret and Prin, and Brucker et al.; see links below.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  gp10-4.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python OpenShop.py -data=<datafile.json>
  python OpenShop.py -data=<datafile.dzn> -parser=OpenShop_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Open-shop_scheduling
  - https://www.sciencedirect.com/science/article/abs/pii/037722179390182M
  - https://link.springer.com/article/10.1023/A:1018930613891
  - https://www.sciencedirect.com/science/article/pii/S0166218X96001163
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  realistic, mzn14
