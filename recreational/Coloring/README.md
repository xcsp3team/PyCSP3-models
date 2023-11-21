# Problem Coloring
## Description

In its simplest form, it is a way of coloring the vertices of a graph such that no two adjacent vertices are of the same color.

## Data
 - nNodes, nColors: the number of nodes and colors
 - edges (tuples of tuples): the list of edges of the graph.

An example is given in the json file.

## Model
  constraints: [Intension](http://pycsp.org/documentation/constraints/Intension), [Maximum](http://pycsp.org/documentation/constraints/Maximum)

## Execution
```
python3 Coloring.py -data=Coloring_rand1.json [-solve]
```

## Links
 - https://en.wikipedia.org/wiki/Graph_coloring

## Tags
 recreational
```

