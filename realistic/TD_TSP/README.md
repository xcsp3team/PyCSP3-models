# Problem TD_TSP

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2017 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  10-24-10.json

## Model
  constraints: [Channel](http://pycsp.org/documentation/constraints/Channel), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TD_TSP.py -data=<datafile.json>
  python TD_TSP.py -data=<datafile.dzn> -parser=TD_TSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn15, mzn17
