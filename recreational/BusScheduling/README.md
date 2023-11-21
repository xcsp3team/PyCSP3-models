# Problem BusScheduling
## Description
Problem 022 of csplib.<br />
Bus driver scheduling can be formulated as a set paritioning problem. These consist of a given set of tasks (pieces of work) to cover and a large set of possible shifts, where each shift covers a subset of the tasks and has an associated cost. We must select a subset of possible shifts that covers each piece of work once and only once: this is called a partition.

## Data

TODO

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Command Line
```
python BusScheduling.py -data=BusScheduling_example.dzn
```

## Links
 - https://www.csplib.org/Problems/prob022/

## Tags
recreational csplib
