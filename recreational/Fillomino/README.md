# Problem: Fillomino

Fillomino is played on a rectangular grid, with some cells containing numbers.
  constraints: [](https://pycsp.org/documentation/constraints/)
  - each clue n is part of a polyomino of size n
  - no two polyominoes of matching size (number of cells) are orthogonally adjacent (share a side)

## Data Example
  08.json

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Fillomino.py -data=<datafile.json>
```

## Links
  - https://en.wikipedia.org/wiki/Fillomino
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  recreational, xcsp24

<br />

## _Alternative Model(s)_

#### Fillomino_z.py
 - constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: recreational, mzn09, mzn11, mzn14
