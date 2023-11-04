# Problem Trucking
## Description
There are some trucks.
Each truck can transport a given Load of material, and has an associated cost.
In each time period a demand has to be fulfilled.
The trucks number 1 and 2 have some further constraints, disallowing them to be used more than once
in consecutive or two consecutive time periods.
The goal is to minimise the overall cost.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
The MZN model was proposed by Jakob Puchinger.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python Trucking.py -data=<datafile.json>
  python Trucking.py -data=<datafile.dzn> -parser=Trucking_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  crafted, mzn08
