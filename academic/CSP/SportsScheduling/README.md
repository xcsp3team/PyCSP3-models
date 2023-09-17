# Problem SportsScheduling
## Description
This is the [problem 010](https://www.csplib.org/Problems/prob010/) of the CSPLib.

The problem is to schedule a tournament of teams over weeks, with each week divided into  periods, and each period divided
into two slots indicating the two involved teams (for example, one playing at home, and the other away). A tournament must satisfy the following three conditions:

 - every team plays every other team.
 - every team plays once a week;
 - every team plays at most twice in the same period over the tournament;

## Data
A number n, the number of teams.

## Model(s)
You can  find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/SportsScheduling/).

There are 2 variants of this problem, one classic and one with dummy variables.

  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Intension](http://pycsp.org/documentation/constraints/Intension), [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Count](http://pycsp.org/documentation/constraints/Count), [Extension](http://pycsp.org/documentation/constraints/Extension)



## Command Line
```
python SportsScheduling.py
python SportsScheduling.py -data=10
python SportsScheduling.py -data=10 -variant=dummy
```

## Tags
 academic notebook
