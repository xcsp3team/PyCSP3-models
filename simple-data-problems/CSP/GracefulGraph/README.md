# Problem Dubois

## Description
This is the [problem 053](https://www.csplib.org/Problems/prob053/) of the CSPLib:

"*A labelling f of the nodes of a graph with q edges is graceful if f assigns each node a unique label from 0, 1...,q 
and when each edge (x,y) is labelled with |f(x)−f(y)|, the edge labels are all different.*"


### Example
Here, is a solution of a $K_4$.

![Graceful Graph](/assets/figures/gracefulgraph.png).



## Data
A couple [k,p] where k is the size of each clique and p is the size of each path (the number of clique).

## Model(s)


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/), [Intension](https://pycsp.org/documentation/constraints/Intension/).



## Command Line


```shell
  python3 GracefulGraph.py
  python3 GracefulGraph.py -data=[3,5]
 ```

## Some Results

| Data   | Number of Solutions |
|--------|---------------------|
| \[3,2] | 96                  | 
| \[3,3] | 6816                | 
| \[2,4] | 1416                | 