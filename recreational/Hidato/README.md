# Problem Hidato
## Description
Hidato, also known as Hidoku is a logic puzzle game invented by Gyora M. Benedek, an Israeli mathematician.
The goal of Hidato is to fill the grid with consecutive numbers that connect horizontally, vertically, or diagonally.

## Data Example
  p1.json

## Model
  Two variants handle differently consecutive numbers:
  - a main variant involving logical (and Count) constraints
  - a variant 'table' involving table constraints

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Count](http://pycsp.org/documentation/constraints/Count), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution (example)
  - python Hidato.py -data=<datafile.json>
  - python Hidato.py -variant=table -data=<datafile.json>
  - python Hidato.py -variant=table -data=[10,10,null]

## Links
  - https://en.wikipedia.org/wiki/Hidato
  - http://www.hidato.com/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
