# Problem KMedian

The k-median problem (with respect to the 1-norm) is the problem of finding k centers such that the clusters formed by them are the most compact.
Formally, given a set of data points, the k centers ci are to be chosen in order to minimize the
sum of the distances from each data point to the nearest ci.

## Data (example)
  pmed01.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python KMedian.py -data=<datafile.json>
  - python KMedian.py -data=<datafile.json> -variant=aux
  - python KMedian.py -data=<datafile.txt> -parser=KMedian_Parser.py

## Links
  -https://en.wikipedia.org/wiki/K-medians_clustering
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  recreational, xcsp23
