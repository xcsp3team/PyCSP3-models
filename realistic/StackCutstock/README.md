# Problem StackCutstock
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  d03.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python StackCutstock.py -data=<datafile.json>
  python StackCutstock.py -data=<datafile.dzn> -parser=StackCutstock_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
