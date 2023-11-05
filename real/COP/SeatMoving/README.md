# Problem SeatMoving
## Description
The problem is to move a person from a start position to a goal position.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Toshimitsu Fujiwara.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  sm-10-11-00.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  python SeatMoving.py -data=sm-10-13-00.json
  python SeatMoving.py -data=sm-10-13-00.dzn -dataparser=SeatMoving_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn18, mzn21
