# Problem: SudokuOpt

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hakan Kjellerstrand (optimization version of the problem, following idea by Mikael Zayenz Lagerkvist).
MIT Licence.

## Data Example
  p20.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SudokuOpt.py -data=<datafile.json>
  python SudokuOpt.py -data=<datafile.dzn> -parser=SudokuOpt_ParserZ.py
```

## Links
  - http://www.hakank.org/minizinc/sudoku_problems2/
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  recreational, mzn22
