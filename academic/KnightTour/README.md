# Problem KnightTour

A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once.
If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately,
following the same path), the tour is closed; otherwise, it is open.

## Data
  A number n, the size of the board.

## Example
  This is an animation on a 5x5 board (source: [wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour))
  ![knight tour](https://upload.wikimedia.org/wikipedia/commons/c/ca/Knights-Tour-Animation.gif)

## Model
  There are two variant, a main one with intensional constraints, and one with table constraints

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python KnightTour.py -data=number
  - python KnightTour.py -data=number -variant=table-2
  - python KnightTour.py -data=number -variant=table-3

## Links
  - https://en.wikipedia.org/wiki/Knight%27s_tour

## Tags
  academic
