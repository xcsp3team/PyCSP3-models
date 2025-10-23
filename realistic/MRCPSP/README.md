# Problem: MRCPSP

Multi-mode Resource-constrained Project Scheduling (MRCPSP)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2023 challenges.
The MZN model was proposed by Ria Szeredi and Andreas Schutt (Copyright: Data61, CSIRO).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  j30-15-05.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MRCPSP.py -data=<datafile.json>
  python MRCPSP.py -data=<datafile.dzn> -parser=MRCPSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn16, mzn23
