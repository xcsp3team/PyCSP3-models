# Problem BnnPlanner
## Description
Planning with Learned Binarized Neural Networks.
See AIJ paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Buser Say.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  sysadmin-4-2S.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python BnnPlanner.py -data=<datafile.json>
  python BnnPlanner.py -data=<datafile.dzn> -parser=BnnPlanner_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0004370220300503
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, mzn20
