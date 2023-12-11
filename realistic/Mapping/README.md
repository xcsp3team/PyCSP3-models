# Problem Mapping
## Description
Mapping an H263 encoder on a system with a network on chip/
This is a simplified version of the model presented in the paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Krzysztof Kuchcinski.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  ring-mp3.json

## Model
  constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Count](http://pycsp.org/documentation/constraints/Count), [Flow](http://pycsp.org/documentation/constraints/Flow), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Mapping.py -data=<datafile.json>
  python Mapping.py -data=<datafile.dzn> -parser=Mapping_ParserZ.py
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0045790614002286
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn15, mzn16, mzn18, mzn21
