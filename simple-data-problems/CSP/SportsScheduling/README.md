
# Problem Social Golfer

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

*Involved Constraints*: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality/),
[Intension](https://pycsp.org/documentation/constraints/Intension/), [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/), 
[Count](https://pycsp.org/documentation/constraints/Count/), [Extension](https://pycsp.org/documentation/constraints/Extension/), [Extension](https://pycsp.org/documentation/constraints/Count/).



## Command Line

By default, SportScheduling.py is in problems/csp/academic directory.

```shell
python SportsScheduling.py
python SportsScheduling.py -data=10
python SportsScheduling.py -data=10 -variant=dummy
 ```

## Some Results
    
| Data | Number of Solutions |
|------|---------------------|
| 6    | 10                  |
| 7    | 5928                |
