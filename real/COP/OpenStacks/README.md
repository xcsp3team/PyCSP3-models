# Problem OpenStacks
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2011/2015 Minizinc challenges.
The MZN model was proposed by Peter J. Stuckey.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  pb-20-20-1.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python OpenStacks.py -data=<datafile.json>
  python OpenStacks.py -data=<datafile.dzn> -parser=OpenStacks_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  real, mzn09, mzn11, mzn15
