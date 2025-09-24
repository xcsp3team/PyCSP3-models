# Problem: Triangular

This problem is taken from Daily Telegraph and Sunday Times.
The problem is to find, for an equilateral triangular grid of size n (length of a side),
the maximum number of nodes that can be selected without having all selected corners of any equilateral triangle
of any size or orientation.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2019/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  An integer n

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Triangular.py -data=number
```

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  academic, mzn15, mzn19, mzn22, mzn24
