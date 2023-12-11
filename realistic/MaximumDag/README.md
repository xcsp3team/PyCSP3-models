# Problem MaximumDag
## Description
Maximum Directed Acyclic Graph.
Given a directed graph G=(V,E) find the subgraph of G that is a DAG, while maximizing the number of edges.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  25-01.json

## Model
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MaximumDag.py -data=<datafile.json>
  python MaximumDag.py -data=<datafile.dzn> -parser=MaximumDag_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  real, mzn16
