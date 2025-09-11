# Problem: SolitairePattern

This is a variant of Peg Solitaire where a goal state (configuration) with a number of pegs in some specific arrangement must be reached.
The initial state is the same as that of central Solitaire (i.e., missing peg in the middle of the board).

The model is written for the English style board (standard), with 33 holes

## Data
  Three integers

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python SolitaireParttern.py -data=[number,number,number]
  python SolitaireParttern.py -data=[number,number,number] -varinat=dec1
  python SolitaireParttern.py -data=[number,number,number] -variant=dec2
  python SolitaireParttern.py -data=[number,number,number] -variant=table
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054805000195
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
