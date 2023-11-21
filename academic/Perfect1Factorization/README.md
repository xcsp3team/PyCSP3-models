# Problem Perfect1Factorization
## Description
A 1-factorization is a partition of the edges of a graph into m-1 complete matchings.
For the 1-factorization to be perfect, every pair of matchings must form a Hamiltonian circuit of the graph.
To make the problem interesting it is specified as an optimization-problem, forcing an ordering on the solutions.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Mikael Zayenz Lagerkvist (Licence at https://github.com/MiniZinc/mzn-challenge/blob/develop/2021/p1f-pjs/LICENSE)

## Data
  an integer n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Channel](http://pycsp.org/documentation/constraints/Channel), [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Perfect1Factorization.py -data=[number]
```

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn09, mzn15, mzn20, mzn21
