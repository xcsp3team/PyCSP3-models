# Problem CyclicRCPSP

This is a cyclic resource-constrained project scheduling problem with generalised precedence relations
constrained to scarce cumulative resources and tasks which are repeated infinitely.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2014 Minizinc challenges.
The original model has: Copyright (C) 2011 The University of Melbourne and NICTA

## Data Example
  easy-4.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum)

## Execution
```
  python CyclicRCPSP.py -data=<datafile.json>
  python CyclicRCPSP.py -data=<datafile.dzn> -parser=CyclicRCPSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn11, mzn14
