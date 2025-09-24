# Problem: GraphClear

Mobile robot graph-clear problem.

In a graph-clear problem, an undirected graph (N,E) with the node weight ai for each node i in N and the edge weight bij for each edge {i,j} in E is given.
In the beginning, all nodes are contaminated. In each step, one node can be made clean by sweeping it using ai robots and blocking each edge {i,j} using bij robots.
However, while sweeping a node, an already swept node becomes contaminated if it is connected by a path of unblocked edges to a contaminated node.
The optimal solution minimizes the maximum number of robots per step to make all nodes clean.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).
This MZN model was mentioned to be adapted from https://github.com/Kurorororo/didp-models/blob/main/graph-clear/graph_clear_cp.py

## Data Example
  n20-2022-14.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python GraphClear.py -data=<datafile.json>
```

## Links
  - https://robotics.ucmerced.edu/sites/g/files/ufvvjh1576/f/page/documents/iros2007c.pdf
  - https://link.springer.com/article/10.1007/s10601-018-9288-3
  - https://github.com/Kurorororo/didp-models/tree/main/graph-clear
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
