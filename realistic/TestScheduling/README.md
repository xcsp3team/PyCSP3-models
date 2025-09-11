# Problem: TestScheduling

This problem was presented as the Industrial Modelling Challenge at the conference CP2015.

From CSPLib: "The problem arises in the context of a testing facility.
A number of tests have to be performed in minimal time.
Each test has a given duration and needs to run on one machine.
While a test is running on a machine, no other test can use that machine.
Some tests can only be assigned to a subset of the machines, for others you can use any available machine.
For some tests, additional, possibly more than one, global resources are needed.
While those resources are used for a test, no other test can use the resource.
The objective is to finish the set of all tests as quickly as possible."

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python TestScheduling.py -data=<datafile.json>
  python TestScheduling.py -data=<datafile.pl> -parser=TestScheduling_Parser.py
```

## Links
  - https://www.csplib.org/Problems/prob073/
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, csplib, xcsp24

<br />

## _Alternative Model(s)_

#### TestScheduling_z.py
 - constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Table](https://pycsp.org/documentation/constraints/Table)
 - tags: realistic, csplib, mzn18, mzn23
