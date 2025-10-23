# Problem: VRP

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The original MZN model was proposed by Jakob Puchinger - no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  P-n20-k2.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python VRP.py -data=<datafile.json>
  python VRP.py -data=<datafile.dzn> -parser=VRP_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Vehicle_routing_problem
  - https://www.minizinc.org/challenge/2013/results/

## Tags
  realistic, mzn09, mzn11, mzn12, mzn13
