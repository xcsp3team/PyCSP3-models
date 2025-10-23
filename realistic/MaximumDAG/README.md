# Problem: MaximumDAG

Maximum Directed Acyclic Graph.
Given a directed graph G=(V,E) find the subgraph of G that is a DAG, while maximizing the number of edges.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  25-01.json

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MaximumDAG.py -data=<datafile.json>
  python MaximumDAG.py -data=<datafile.dzn> -parser=MaximumDAG_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2016/results/

## Tags
  realistic, mzn16
