# Problem: DiamondFree

A diamond is a set of four vertices in a graph such that there are at least five edges between those vertices.
Conversely, a graph is diamond-free if it has no diamond as an induced subgraph, i.e. for every set of four vertices
the number of edges between those vertices is at most four.

See Problem 050 on CSPLib

## Data
  a unique integer, the order of the problem instance

### Example
  For n=9, a solution is
  ```
   6 6 6 3 3 3 3 3 3   # the degree of vertices

   0 0 0 1 1 1 1 1 1
   0 0 0 1 1 1 1 1 1
   0 0 0 1 1 1 1 1 1
   1 1 1 0 0 0 0 0 0
   1 1 1 0 0 0 0 0 0
   1 1 1 0 0 0 0 0 0
   1 1 1 0 0 0 0 0 0
   1 1 1 0 0 0 0 0 0
   1 1 1 0 0 0 0 0 0
  ```

  A representation of the graph is here:
    ![diamondfree](https://pycsp.org/assets/figures/diamondfree.png)

## Model
  constraints: [Lex](https://pycsp.org/documentation/constraints/Lex), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python DiamondFree.py -data=number
```

## Links
  - https://www.csplib.org/Problems/prob050/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, csplib, xcsp22
