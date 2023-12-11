# Problem GeneralizedMKP
## Description
In this variation of the knapsack problem, the weight of knapsack item i is given by a D-dimensional vector
wi = (wi1 , . . . , wiD ) and the knapsack has a D-dimensional capacity vector (W1 , . . . , WD ).
The target is to maximize the sum of the values of the items in the knapsack so that
the sum of weights in each dimension d does not exceed Wd .
See Wikipedia.

## Data (example)
  OR05x100-25-1.json

## Model
  constraints: [Knapsack](http://pycsp.org/documentation/constraints/Knapsack), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python GeneralizedMKP.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Knapsack_problem
  - https://www.researchgate.net/publication/271198281_Benchmark_instances_for_the_Multidimensional_Knapsack_Problem
  - https://www.minizinc.org/challenge2019/results2019.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, mzn15, mzn19, xcsp23
