# Problem Graph Coloring

## Description

See [wikipedia](https://en.wikipedia.org/wiki/Graph_coloring): In its simplest form, it is a way of coloring the vertices of a graph such that no two adjacent vertices are of the same color.



## Data

 - nNodes, nColors: the number of nodes and colors
 - edges (tuples of tuples): the list of edges of the graph. 

An example is given in the json file.
## Model


*Involved Constraints*: [Maximum](https://pycsp.org/documentation/constraints/Maximum)


## Command Line

```shell
python3 Coloring.py -data=Coloring_rand1.json [-solve]
```


