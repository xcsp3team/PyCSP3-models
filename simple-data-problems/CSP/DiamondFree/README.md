# Problem Diamond Free

## Description

This is the [problem 050](https://www.csplib.org/Problems/prob050/) of the CSPLib. You can find a short description 
below: 

Given a graph with set n vertices. The problem is produce all unique degree sequences $d_1,...d_n$, such that

 - $d_i\geq d_i+1$ 
 - each degree $d_i>0$
 - and $d_i$ is modulo 3
 - the sum of the degrees is modulo 12
 - there exists a simple diamond-free graph with that degree sequence, i.e.  for every set of four vertices the number of edges between those vertices is at most four.
 
### Example

For n=9, a solution is 
```
  6 6 6 3 3 3 3 3 3   # the degree of vertices

  0 0 0 1 1 1 1 1 1
  0 0 0 1 1 1 1 1 1
  0 0 0 1 1 1 1 1 1
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
```

A representation of the graph is here: 

![assets/](https://pycsp.org/assets/figures/diamondfree.png)

## Data
A number n, the number of nodes of the graph.

## Model(s)



*Involved Constraints*: [Sum](https://pycsp.org/documentation/constraints/Sum/), [Intension](https://pycsp.org/documentation/constraints/Intension/),
[Decreasing](https://pycsp.org/documentation/constraints/Decreasing/), [LexIncreasing](https://pycsp.org/documentation/constraints/LexIncreasing/).



## Command Line

```shell
python DiamondFree.py
python DiamondFree.py -data=10
```

## Some Results

| Data | Number of Solutions |
|--|---------------------|
| 6 | 0                  |
| 8 | 17                  |
| 9 | 1                |
| 10 | 1                  |

