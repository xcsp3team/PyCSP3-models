# Problem SportsScheduling
## Description
This is the [problem 010](https://www.csplib.org/Problems/prob010/) of the CSPLib.

The problem is to schedule a tournament of teams over weeks, with each week divided into  periods, and each period divided
into two slots indicating the two involved teams (for example, one playing at home, and the other away). A tournament must satisfy the following three conditions:

 - every team plays every other team.
 - every team plays once a week;
 - every team plays at most twice in the same period over the tournament;

## Data
  an integer n, the number of teams

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Count](http://pycsp.org/documentation/constraints/Count), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python SportScheduling.py -data=[number]
  - python SportsScheduling.py -variant=table -data=[number]

## Links
  - https://www.csplib.org/Problems/prob026/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp


## Tags
 academic notebook csplib
