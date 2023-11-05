# Problem JavaRouting
## Description
The model, below, is rebuilt from instances submitted to the 2013/2021 Minizinc challenges.
These instances are initially automatically generated from a problem description in Java.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  trip6-3.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element)

## Execution
```
  python JavaRouting.py -data=<datafile.json>
  python JavaRouting.py -data=<datafile.dzn> -parser=JavaRouting_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn13, mzn21
