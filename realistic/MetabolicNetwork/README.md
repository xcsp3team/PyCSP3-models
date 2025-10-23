# Problem: MetabolicNetwork

The model, below, is close to (can be seen as the close translation of) the one (called network_50) submitted to the 2024 Minizinc challenges.
The original MZN model is accompanied with a MIT Licence (Copyright 2024 Maxime Mahout, François Fages).

## Data Example
  09.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MetabolicNetwork.py -data=<datafile.json>
  python MetabolicNetwork.py -data=<datafile.json> -parser=MetabolicNetwork_Converter.py
  python MetabolicNetwork.py -data=<datafile.dzn> -parser=MetabolicNetwork_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2024/results/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, mzn24, xcsp25
