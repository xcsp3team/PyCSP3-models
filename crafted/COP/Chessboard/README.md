# Problem Chessboard
## Description
Place knights, rooks, queens, bishops on a n*n chessboard so that none takes each other.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Chessboard.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  crafted, mzn23
