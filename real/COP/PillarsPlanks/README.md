# Problem PillarsPlanks
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  p-d02.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python PillarsPlanks.py -data=<datafile.json>
  python PillarsPlanks.py -data=<datafile.dzn> -parser=PillarsPlanks_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, mzn20
