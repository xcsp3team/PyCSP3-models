# Problem SocialGolfers
## Description
This is the [problem 010](https://www.csplib.org/Problems/prob010/) of the CSPLib.

"*The coordinator of a local golf club has come to you with the following problem. In their club, there are 32 social golfers, e
ach of whom play golf once a week, and always in groups of 4. They would like you to come up with a schedule of play for these golfers,
to last as many weeks as possible, such that no golfer plays in the same group as any other golfer on more than one occasion.
The problem can easily be generalized to that of scheduling groups of golfers over at most weeks, such
that no golfer plays in the same group as any other golfer twice (i.e. maximum socialisation is achieved).
For the original problem, the values of and are respectively 8 and 4.*".

## Data
A triplet \[n,s,w], n is the number of groups, s the size of the groups and w the number of weeks.

## Model(s)
You can  find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/SocialGolfers/).

There are 2 variants of this problem one with constraints sum the other with constraints in intension.

  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Intension](http://pycsp.org/documentation/constraints/Intension), [Sum](http://pycsp.org/documentation/constraints/Sum), [LexIncreasing](http://pycsp.org/documentation/constraints/LexIncreasing)

## Command Line
```
python SocialGolfers.py
python SocialGolfers.py -data=[5,3,6]
python SocialGolfers.py -data=[5,3,6] -variant=1
```

## Tags
 academic notebook csplib
