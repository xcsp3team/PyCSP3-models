# Problem: CityPosition

The problem si to determine city positions using road distances (like MDS plotting but allows missing values).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  5-05.json

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CityPosition.py -data=<datafile.json>
  python CityPosition.py -data=<datafile.dzn> -parser=CityPosition_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2017/results/

## Tags
  realistic, mzn17
