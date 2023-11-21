# Problem CVRP
## Description
Capacitated Vehicle Routing problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
The MZN model was proposed by Andrea Rendl (CP formulation adapted to use instances for MIP models).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  A-n37-k5.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CVRP.py -data=<datafile.json>
  python CVRP.py -data=<datafile.dzn> -parser=CVRP_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Vehicle_routing_problem
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  real, mzn15
