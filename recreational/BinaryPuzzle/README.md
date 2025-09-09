# Problem: BinaryPuzzle

A binary puzzle (also known as a binary Sudoku) is a puzzle played on an n × n grid;
initially some of the cells may contain 0 or 1 (but this is not the case for the 2023 competition).
One has to fill the remaining empty cells with either 0 or 1 according to the following rules:
  -  no more than two similar numbers next to or below each other are allowed,
  -  each row and each column should contain an equal number of zeros and ones,
  - each row is unique and each column is unique.

## Data
  A unique integer n

## Model
  constraints: [AllDifferentList](https://pycsp.org/documentation/constraints/AllDifferentList), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python BinaryPuzzle.py -data=number
  python BinaryPuzzle.py -data=number -variant=regular
```

## Links
  - https://www.researchgate.net/publication/243972408_Binary_Puzzle_is_NP-complete
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
