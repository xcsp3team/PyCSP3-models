# Problem Fillomino

Fillomino is played on a rectangular grid, with some cells containing numbers.
The goal is to divide the grid into regions called polyominoes (by filling in their boundaries)
  constraints: [](http://pycsp.org/documentation/constraints/)
  - each clue n is part of a polyomino of size n
  - no two polyominoes of matching size (number of cells) are orthogonally adjacent (share a side)

## Data Example
  08.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Fillomino.py -data=<datafile.json>
```

## Links
  - https://en.wikipedia.org/wiki/Fillomino

## Tags
  recreational

<br />

## _Alternative Model(s)_

#### Fillomino_z.py
 - constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: recreational, mzn09, mzn11, mzn14
