# Problem CableTreeWiring
## Description
Deriving the optimal wiring sequence for a given layout of a cable tree.
See paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  A031.json

## Model
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python CableTreeWiring.py -data=<datafile.json>
  python CableTreeWiring.py -data=<datafile.dzn> -parser=CableTreeWiring_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-021-09321-w
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, mzn20
