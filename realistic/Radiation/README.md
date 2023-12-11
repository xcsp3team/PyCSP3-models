# Problem Radiation
## Description
The problem of decomposing an integer matrix into a weighted sum of binary matrices has received much attention in recent years,
largely due to its application in radiation treatment for cancer.
See paper whose reference is given below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Sebastian Brand.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  m06-15-15.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Radiation.py -data=<datafile.json>
  python Radiation.py -data=<datafile.dzn> -parser=Radiation_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1007/s10601-010-9104-1
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  real, mzn08, mzn12, mzn13, mzn15, mzn20
