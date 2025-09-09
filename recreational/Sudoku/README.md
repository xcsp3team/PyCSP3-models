# Problem: Sudoku

The famous logic puzzle. See, e.g., "Sudoku as a Constraint Problem" by Helmut Simonis

## Data Example
  s13a.json

## Model
  There exists different variant.

  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python Sudoku.py -data=[number,None]
  python Sudoku.py -data=<datafile.json>
  python Sudoku.py -data=<datafile.json> -variant=table
  python Sudoku.py -data=<datafile.txt> -parser=Sudoku_Parser.py
```

## Links
 - https://en.wikipedia.org/wiki/Sudoku
 - https://www.semanticscholar.org/paper/Sudoku-as-a-Constraint-Problem-Simonis/4f069d85116ab6b4c4e6dd5f4776ad7a6170faaf

## Tags
  recreational, notebook
