# Problem: Gametes

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The original model was written by Kelvin Davis (MIT Licence).

## Data Example
  nl07-m10-134.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Gametes.py -data=<datafile.json>
```

## Links
  - https://mssanz.org.au/modsim2023/files/davis.pdf
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn23
