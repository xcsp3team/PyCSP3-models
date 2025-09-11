# Problem: HyperSudoku

Hyper Sudoku differs from Sudoku by having additional constraints.
When the base of the grid is 3 (as usually for Sudoku) there are four 3-by-3 blocks in addition to the major 3-by-3 blocks
that also require exactly one entry of each numeral from 1 through 9.

The model is given below for an empty grid (no clues).

## Data
  an integer

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent)

## Execution:
```
  python HyperSudoku.py -data=number
```

## Links
  - https://en.wikipedia.org/wiki/Sudoku
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, recreational, xcsp24
