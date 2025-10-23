# Problem: BusScheduling

Problem 022 of csplib.

Bus driver scheduling can be formulated as a set partitioning problem.
These consist of a given set of tasks (pieces of work) to cover and a large set of possible shifts, where each shift covers a subset of the tasks
and has an associated cost. We must select a subset of possible shifts that covers each piece of work once and only once: this is called a partition.

## Data Illustration
  t1.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python BusScheduling.py -data=<datafile.json>
```

## Links
 - https://www.csplib.org/Problems/prob022/
 - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, csplib, xcsp25
