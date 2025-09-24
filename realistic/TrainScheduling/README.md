# Problem: TrainScheduling

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  05.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TrainScheduling.py -data=<datafile.json>
  python TrainScheduling.py -data=<datafile.dzn> -parser=TrainScheduling_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
