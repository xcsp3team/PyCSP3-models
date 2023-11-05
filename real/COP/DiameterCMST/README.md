# Problem DiameterCMST
## Description
Diameter Constrained Minimum Spanning Tree.
Given an undirected graph G=(V,E) and an integer k find a spanning tree of G of minimum cost such that its diameter is not greater than k.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  c-v15-a105-d6.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python DiameterCMST.py -data=<datafile.json>
  python DiameterCMST.py -data=<datafile.dzn> -parser=DiameterCMST_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  real, mzn16, mzn22
