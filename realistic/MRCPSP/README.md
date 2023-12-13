# Problem MRCPSP
## Description
Multi-mode Resource-constrained Project Scheduling (MRCPSP)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2023 challenges.
The MZN model was proposed by Ria Szeredi and Andreas Schutt (Copyright: Data61, CSIRO).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  j30-15-5.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MRCPSP.py -data=<datafile.json>
  python MRCPSP.py -data=<datafile.dzn> -parser=MRCPSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn16, mzn23
