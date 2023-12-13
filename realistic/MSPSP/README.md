# Problem MSPSP
## Description
Multi-Skilled Project Scheduling Problem

This is a variation of the basic resource-constrained project scheduling problem.
A set of activities must be executed so that the project duration is minimised while satisfying:
  - precedence relations between some activities expressing that an activity can only be run after its preceding activity's execution is finished,
  - skills requirements of activities on workers who have the capability to  perform the activity,
  - workers availability, i.e., a worker can perform only one activity in each time period.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  easy-01.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MSPSP.py -data=<datafile.json>
  python MSPSP.py -data=<datafile.dzn> -parser=MSPSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
