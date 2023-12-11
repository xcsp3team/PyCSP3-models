# Problem SteinerTree
## Description
Steiner Tree Problem: find a tree in a graph containing all the "terminal" nodes while minimizing its weight.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Diege de Una.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  es10fst03.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SteinerTree.py -data=<datafile.json>
  python SteinerTree.py -data=<datafile.dzn> -parser=SteinerTree_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn18
