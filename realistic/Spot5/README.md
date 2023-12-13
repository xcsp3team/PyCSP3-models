# Problem Spot5
## Description
SPOT5 earth observation satellite management problem.

The  management problems  to  be solved  can  be roughly  described as follows:
  - given a set S of photographs which can be taken the next day from at least one of the three instruments, wrt the satellite trajectory;
  - given, for each photograph, a weight expressing its importance;
  constraints: [](http://pycsp.org/documentation/constraints/), [non overlapping and minimal transition time between two successive photographs on the same instrument](http://pycsp.org/documentation/constraints/non overlapping and minimal transition time between two successive photographs on the same instrument)
   limitation on the instantaneous data flow through the satellite telemetry and on the recording capacity on board;
  - find an admissible subset S' of S (imperative  constraints set) which maximizes the sum of the weights of the photographs in S'.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2015/2022 Minizinc challenges.
The MZN model was proposed by Simon de Givry.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  not shown because large data files

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Spot5.py -data=<datafile.json>
  python Spot5.py -data=<datafile.dzn> -parser=Spot5_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1023/A:1026488509554
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn14, mzn15, mzn22
