# Problem BusScheduling

## Description
[Problem 022](https://www.csplib.org/Problems/prob022/data/bus_scheduling_csplib_t1.dzn.html) of the CSPLib:
Bus driver scheduling can be formulated as a set paritioning problem. These consist of a given set of tasks (pieces of work) to cover and a large set of possible shifts, where each shift covers a subset of the tasks and has an associated cost. We must select a subset of possible shifts that covers each piece of work once and only once: this is called a partition.



## Data



## Model

*Involved Constraints*: [Sum](https://pycsp.org/documentation/constraints/Sum) [Count](https://pycsp.org/documentation/constraints/Count)


## Command Line

```shell
python3 BusScheduling.py -data=BusScheduling_example.dzn [-solve]
```


