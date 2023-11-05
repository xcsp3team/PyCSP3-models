# Problem ValveNetwork
## Description
This is a model for the Valve network planning for Advent of Code 2022 Day 16.
Instead of using different networks for varying hardness, this model uses different planning horizons for adjusting the hardness of the problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.

## Data
  an integer (as the network is included in the model below)

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  python ValveNetwork.py -data=6

## Links
  - https://adventofcode.com/2022
  - https://github.com/zayenz/advent-of-code-2022
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  real, mzn23
