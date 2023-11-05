# Problem RotatingWorkforce
## Description
Rotating Workforce Scheduling.

The problem aims to schedule workers satisfying shift sequence constraints while ensuring that enough shifts are covered on each day.
All workers complete the same schedule, just starting at different days.
See CPAIOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2019 Minizinc challenges.
The MZN model was proposed by Andreas Schutt.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  0103.json

## Model
  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Regular](http://pycsp.org/documentation/constraints/Regular)

## Execution
  python RotatingWorkforce.py -data=<datafile.json>
  python RotatingWorkforce.py -data=<datafile.dzn> -parser=RotatingWorkforce_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-93031-2_31
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn18, mzn19
