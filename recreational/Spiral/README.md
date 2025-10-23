# Problem: Spiral

From Peter Szeredi (see paper cited below):
In this puzzle, a square board of n ∗ n cells is given.
The task is to place integer numbers, chosen from the range 1..m (we have m ≤ n), on certain cells of the board, so that the following conditions hold:
  - in each row and each column all integers in 1..m occur exactly once, and there are n − m empty cells;
  - along the spiral starting from the top left corner, the integers follow the pattern 1, 2, ..., m, 1, 2, ... , m, ... (number m is called the period of the spiral).
Initially, some numbers may be already placed on the board.

## Data
  Two integers n and m.

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality)

## Execution
```
  python Spiral.py
  python Spiral.py -data=[number,number]
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24662-6_11

## Tags
  academic, recreational
