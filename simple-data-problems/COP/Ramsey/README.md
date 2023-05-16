
# Problem Ramsey

## Description
This is the [problem 017](https://www.csplib.org/Problems/prob017/) of the CSPLib:

The edges of a complete graph (with n nodes) must be coloured with the minimum number of colours.
There must be no monochromatic triangle in the graph, i.e. in any triangle at most two edges have the same colour.
With 3 colours, the problem has a solution if n < 17.





## Data
A number n, the number of nodes of the graph.

## Model(s)

*Involved Constraints*: [NValues](https://pycsp.org/documentation/constraints/NValues/), [Maximum](https://pycsp.org/documentation/constraints/Maximum/).


## Command Line

```
python Ramsey.py
python Ramsey.py -data=10
```

## Some Results



| Data | Optimum |
|------|---------|
| 8    | 2       |
| 9    | 2       |
| 10   | 2       |
