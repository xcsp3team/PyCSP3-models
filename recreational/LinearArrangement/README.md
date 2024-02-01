# Problem LinearArrangement

For a given (undirected) graph G, the problem consists in arranging the nodes of the graph in a line
in such a way to minimize the sum of distances between adjacent nodes (in G).

## Data
  MinLA01.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python3 LinearArrangement.py -data=<datafile.json>
```

## Tags
  recreational
