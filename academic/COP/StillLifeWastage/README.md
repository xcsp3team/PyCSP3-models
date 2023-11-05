# Problem StillLifeWastage
## Description
The Maximum Density Sill-Life Problem is to fill an n ×n board of cells with the maximum number of live cells
so that the board is stable under the rules of Conway’s Game of Life.
In the CP conference paper (whose reference is given below), the problem is to minimise “wastage” instead.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  an integer n, the order of the problem instance

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python StillLifeWastage.py -data=[number]

## Links
  - https://en.wikipedia.org/wiki/Still_life_(cellular_automaton)
  - https://link.springer.com/chapter/10.1007/978-3-642-04244-7_22
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  academic, mzn12
