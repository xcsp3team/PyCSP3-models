# Problem: JavaRouting

The model, below, is rebuilt from instances submitted to the 2013/2021 Minizinc challenges.
These instances are initially automatically generated from a problem description in Java.
For the original DZN files, no licence was explicitly mentioned (MIT Licence assumed).

The model, below, is an attempt to rebuild the original model from DZN files.
Unfortunately, we didn't find any information about the origin of this problem/model.

## Data Example
  trip6-3.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element)

## Execution
```
  python JavaRouting.py -data=<datafile.json>
  python JavaRouting.py -data=<datafile.dzn> -parser=JavaRouting_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn13, mzn21
