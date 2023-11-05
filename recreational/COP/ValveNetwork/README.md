# Problem ValveNetwork
## Description
This is a model for the Valve network planning for Advent of Code 2022 Day 16.
The original model has been written by Mikael Zayenz Lagerkvist for the Minizinc challenge 2023.

Instead of using different networks for varying hardness,
this model uses different planning horizons for adjusting the hardness of the problem.

## Data
  an integer (as the network is included in the model below)

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Extension](http://pycsp.org/documentation/constraints/Extension), [Intension](http://pycsp.org/documentation/constraints/Intension), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ValveNetwork.py -data=6
```

## Links
  - https://adventofcode.com/2022
  - https://github.com/zayenz/advent-of-code-2022
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  real, mzn23
