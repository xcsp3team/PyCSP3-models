# Problem: Chessboard

Place knights, rooks, queens, bishops on an n*n chessboard so that none takes each other.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Chessboard.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  recreational, mzn23
