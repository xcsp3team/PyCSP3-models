# Problem: StableGoods

The model (main variant), below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  s-d06.json

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python StableGoods.py -data=<datafile.json>
  python StableGoods.py -data=<datafile.dzn> -parser=StableGoods_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2020/results/

## Tags
  realistic, mzn20
