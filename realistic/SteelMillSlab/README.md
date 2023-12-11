# Problem SteelMillSlab
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  13-0.json

## Model
  constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SteelMillSlab.py -data=<datafile.json>
  python SteelMillSlab.py -data=<datafile.dzn> -parser=SteelMillSlab_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob038/
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  real, csplib, mzn17, mzn19
