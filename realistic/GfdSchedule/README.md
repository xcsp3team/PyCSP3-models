# Problem: GfdSchedule

A Scheduling problem, such that:
 - items are grouped by kinds
 - items are processed by groups using facilities
 - items must be processed after some 'produced days'
 - the maximum number of processed-items/day is fixed
 - the objective:
   a) items may be processed before 'deadLineDay'
   b) minimizing groups (minimizing use of facilities)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n025f5d20m10k3.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [NValues](https://pycsp.org/documentation/constraints/NValues), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python GfdSchedule1.py -data=<datafile.json>
  python GfdSchedule1.py -data=<datafile.dzn> -parser=GfdSchedule_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2015/results/

## Tags
  realistic, mzn15

<br />

## _Alternative Model(s)_

#### GfdSchedule2.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn16, mzn18, mzn22
