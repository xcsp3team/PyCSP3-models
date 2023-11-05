# Problem SudokuOpt
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hakan Kjellerstrand (optimization version of the problem, following idea by Mikael Zayenz Lagerkvist).
MIT Licence.

## Data Example
  p20.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python SudokuOpt.py -data=sm-10-13-00.json
  python SudokuOpt.py -data=sm-10-13-00.dzn -dataparser=SudokuOpt_ParserZ.py

## Links
  - http://www.hakank.org/minizinc/sudoku_problems2/
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn22
