# Problem VRP
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Jakob Puchinger.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  A-n38-k5.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python VRP.py -data=<datafile.json>
  python VRP.py -data=<datafile.dzn> -parser=VRP_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Vehicle_routing_problem
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  real, mzn09, mzn11, mzn12, mzn13
