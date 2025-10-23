# Problem: TeamAssignment

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2022 Minizinc challenges.
The original MZN model was proposed by Erik Thörnbald (Uppsala University) - no licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  2-5-6.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [BinPacking](https://pycsp.org/documentation/constraints/BinPacking), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TeamAssignment.py -data=<datafile.json>
  python TeamAssignment.py -data=<datafile.dzn> -parser=TeamAssignment_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn18, mzn22
