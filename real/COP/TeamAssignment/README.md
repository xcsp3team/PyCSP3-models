# Problem TeamAssignment
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2022 Minizinc challenges.
The MZN model was proposed by Erik Thörnbald (Uppsala University).
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  1-6-24.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python TeamAssignment.py -data=<datafile.json>
  python TeamAssignment.py -data=<datafile.dzn> -parser=TeamAssignment_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  real, mzn18, mzn22
