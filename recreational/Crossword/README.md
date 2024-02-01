# Problem Crossword

Given a grid with imposed black cells (spots) and a dictionary, the problem is to fulfill the grid with the words contained in the dictionary.

## Data Example
  vg0607-ogd.json

## Model
  Two variants are defined from different angles:
  - a main variant where variables correspond to letters
  - a variant 'alt' where variables correspond to words

  constraints: [AllDifferentList](http://pycsp.org/documentation/constraints/AllDifferentList), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python Crossword.py -data=<datafile.json>
  - python Crossword.py -data=<datafile.json> -variant=alt
  - python Crossword.py -data=[vg0405,dict=ogd2008] -parser=Crossword_Parser.py

## Links
  - https://www.researchgate.net/publication/221442491_Constraint_Programming_Lessons_Learned_from_Crossword_Puzzles
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
