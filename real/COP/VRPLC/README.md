# Problem VRPLC
## Description
The Vehicle Routing Problem with Location Congestion (VRPLC) adds cumulative scheduling constraints
on to the standard Pickup and Delivery Problem with Time Windows (PDPTW).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Edward Lam, and described in the 2016 paper of Constraints Journal (see below).
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  09-5-10-s1.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python VRPLC.py -data=<datafile.json>
  python VRPC.py -data=<datafile.dzn> -parser=VRPLC_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-016-9241-2
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn18, mzn23
