# Problem: Hidato

Hidato, also known as Hidoku is a logic puzzle game invented by Gyora M. Benedek, an Israeli mathematician.
The goal of Hidato is to fill the grid with consecutive numbers that connect horizontally, vertically, or diagonally.

## Data Example
  p1.json

## Model
  Two variants handle differently consecutive numbers:
  - a main variant involving logical (and Count) constraints
  - a variant 'table' involving table constraints

  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Hidato.py -data=<datafile.json>
  python Hidato.py -data=<datafile.json> -variant=table
  python Hidato.py -data=[number,number,null] -variant=table
```

## Links
  - https://en.wikipedia.org/wiki/Hidato
  - http://www.hidato.com/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
