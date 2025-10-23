# Problem: Smelt

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  02.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Smelt.py -data=<datafile.json>
  python Smelt.py -data=<datafile.dzn> -parser=Smelt_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  realistic, mzn14
