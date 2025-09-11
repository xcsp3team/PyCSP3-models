# Problem: LitPuzzle

5x5 puzzle, by Martin Chlond (and mentioned by Håkan Kjellerstrand on his website).

Each of the squares in the grid (n by n) can be in one of two states, lit (white) or unlit (red).
If the player clicks on a square then that square and each orthogonal neighbour will toggle between the two states.
Each mouse click constitutes one move and the objective of the puzzle is to light all squares in the least number of moves.

## Data
  a number n

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python LitPuzzle.py -data=number
```

## Links
  - https://www.hakank.org/webblogg/archives/001229.html
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
