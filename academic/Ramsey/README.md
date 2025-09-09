# Problem: Ramsey

This is [Problem 017](https://www.csplib.org/Problems/prob017/) at CSPLib.

The edges of a complete graph (with n nodes) must be coloured with the minimum number of colours.
There must be no monochromatic triangle in the graph, i.e. in any triangle at most two edges have the same colour.
With 3 colours, the problem has a solution if n < 17.

## Data
  A number n, the number of nodes of the graph.

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [NValues](https://pycsp.org/documentation/constraints/NValues)

## Execution
```
  python Ramsey.py -data=number
```

## Tags
  academic, csplib
