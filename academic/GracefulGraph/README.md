# Problem: GracefulGraph

This is Problem 053 at CSPLib.

A labelling f of the nodes of a graph with q edges is graceful if f assigns each node a unique label from 0, 1...,q
and when each edge (x,y) is labelled with |f(x)−f(y)|, the edge labels are all different.

## Data
  A pair (k,p) where k is the size of each clique and p is the size of each path (the number of clique).

## Example
  Here, is a solution of a K_4.
  ![Graceful Graph](/assets/figures/gracefulgraph.png).

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent)

## Execution
```
  python GracefulGraph.py -data=[number,number]
```

### Links
  - https://www.csplib.org/Problems/prob053

## Tags
  academic, csplib
