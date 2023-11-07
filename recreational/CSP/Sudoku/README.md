# Problem Sudoku
## Description
The famous logic puzzle. See, e.g., "Sudoku as a Constraint Problem" by Helmut Simonis

## Data
TODO + parser

## Model
There exists different variant.

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python3 Sudoku.py -data=[9,None]
  python3 Sudoku.py -data=Sudoku_s13a.json
  python3 Sudoku.py -data=Sudoku_s13a.json -variant=table
  python3 Sudoku.py -data=Sudoku_example.txt -dataparser=Sudoku_Parser.py
```

## Links
 - https://en.wikipedia.org/wiki/Sudoku

## Tags
  recreational
