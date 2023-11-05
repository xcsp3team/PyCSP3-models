# Problem Filters
## Description
This problem is about optimizing the scheduling of filter operations, commonly used in High-Level Synthesis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Krzysztof Kuchcinski.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  ar2-3.json

## Model
  constraints: [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Maximum](http://pycsp.org/documentation/constraints/Maximum)

## Execution
  python Filters.py -data=<datafile.json>
  python Filters.py -data=<datafile.dzn> -parser=Filters_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S1383762103000754
  - https://github.com/radsz/jacop/tree/develop/src/main/java/org/jacop/examples/fd/filters
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  real, mzn10, mzn12, mzn13, mzn16
