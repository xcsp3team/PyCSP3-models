# Problem Ramsey
## Description
This is the [problem 017](https://www.csplib.org/Problems/prob017/) of the CSPLib:

The edges of a complete graph (with n nodes) must be coloured with the minimum number of colours.
There must be no monochromatic triangle in the graph, i.e. in any triangle at most two edges have the same colour.
With 3 colours, the problem has a solution if n < 17.


## Data
A number n, the number of nodes of the graph.

## Model(s)

  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NValues](http://pycsp.org/documentation/constraints/NValues)


## Command Line

```
python Ramsey.py
python Ramsey.py -data=10
```

## Tags
 academic csplib
