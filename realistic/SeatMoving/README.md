# Problem: SeatMoving

The problem is to move a person from a start position to a goal position.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Toshimitsu Fujiwara.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  sm-10-12-00.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python SeatMoving.py -data=sm-10-13-00.json
  python SeatMoving.py -data=sm-10-13-00.dzn -dataparser=SeatMoving_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn18, mzn21
