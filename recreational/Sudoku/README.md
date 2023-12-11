# Problem Sudoku
## Description
The famous logic puzzle. See, e.g., "Sudoku as a Constraint Problem" by Helmut Simonis

## Data Example
  s13a.json

## Model
  There exists different variant.

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python Sudoku.py -data=[9,None]
  python Sudoku.py -data=<datafile.json>
  python Sudoku.py -data=<datafile.json> -variant=table
  python Sudoku.py -data=<datafile.txt> -dataparser=Sudoku_Parser.py
```

## Links
 - https://en.wikipedia.org/wiki/Sudoku

## Tags
  recreational
