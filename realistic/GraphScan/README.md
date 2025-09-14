# Problem: GraphScan

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The original model seems to have been written by Peter Schneider-Kamp (MIT Licence assumed).

## Data
  n10-p1500-c15.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum)

## Execution
```
  python GraphScan.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
