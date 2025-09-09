# Problem: Dominoes

You are given a grid of size n × m containing numbers being parts of dominoes.
For example, for n = 7 and m = 8, the grid contains all dominoes from 0-0 to 6-6.
One has to find the position (and rotation) of each domino.

# Data Example
  grid01.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Dominoes.py -data=<datafile.json>
  python Dominoes.py -data=<datafile.json> -variant=table
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24662-6_11
  - https://www.researchgate.net/publication/266585191_Dominoes_as_a_Constraint_Problem
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  recreational, xcsp23
