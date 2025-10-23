# Problem: WMSC

Weighted multi-set cover.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Mikael Zayenz Lagerkvist.
The model and the instances are extracted from an industrial use-case.
MIT License.

## Data
  b0-c253-i6-small-cost-e4-sr472-cd16.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python WMSC.py -data=b0_c115_i1_base_full_e3_sr702_cd86.json
  python WMSC.py -data=b0_c115_i1_base_full_e3_sr702_cd86.dzn -dataparser=WMSC_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2021/results/

## Tags
  realistic, mzn21
