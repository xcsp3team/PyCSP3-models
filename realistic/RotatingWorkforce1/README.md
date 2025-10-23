# Problem: RotatingWorkforce1

Rotating Workforce Scheduling.

The problem aims to schedule workers satisfying shift sequence constraints while ensuring that enough shifts are covered on each day.
All workers complete the same schedule, just starting at different days.
See CPAIOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2019 Minizinc challenges.
The original MZN model was proposed by Andreas Schutt - no licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  0103.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RotatingWorkforce1.py -data=<datafile.json>
  python RotatingWorkforce1.py -data=<datafile.dzn> -parser=RotatingWorkforce1_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-93031-2_31
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn18, mzn19
