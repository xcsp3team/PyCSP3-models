# Problem: AlteredStates

From JaneStreet:
    Enter letters into a n×n grid above to achieve the highest score you can.
    You earn points for each of the 50 U.S. states present in your grid.
      - states can be spelled by making King’s moves from square to square
      - the score for a state is its length (main variant)
      - if a state appears multiple times in your grid, it only scores once

## Data
  a number n

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Lex](https://pycsp.org/documentation/constraints/Lex), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python AlteredStates.py -data=number
  python AlteredStates.py -data=number -variant=bis
```

## Links
  - https://www.janestreet.com/puzzles/altered-states-index/
  - https://www.janestreet.com/puzzles/altered-states-2-index/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, janestreet, xcsp25
