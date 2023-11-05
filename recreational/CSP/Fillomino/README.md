# Problem Fillomino
## Description
Fillomino is played on a rectangular grid, with some cells containing numbers.
The goal is to divide the grid into regions called polyominoes (by filling in their boundaries)
  constraints: [](http://pycsp.org/documentation/constraints/)
  - each clue n is part of a polyomino of size n
  - no two polyominoes of matching size (number of cells) are orthogonally adjacent (share a side)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2011/2014 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  08.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Fillomino.py -data=<datafile.json>
  python Fillomino.py -data=<datafile.dzn> -parser=Fillomino_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Fillomino
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  recreational, mzn09, mzn11, mzn14
