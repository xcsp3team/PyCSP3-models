# Problem GeneralizedBACP
## Description
Generalised Balanced Academic Curriculum problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2017/2020 Minizinc challenges.
The MZN model was proposed by Jean-Noel Monette, and modified by Gustav Bjordal with help by Fatima Zohra Lebbah, Justin Pearson, and Pierre Flener.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  UD3.json

## Model
  constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python GeneralizedBACP.py -data=<datafile.json>
  python GeneralizedBACP.py -data=<datafile.dzn> -parser=GeneralizedBACP_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob064/
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, csplib, mzn16, mzn17, mzn20
