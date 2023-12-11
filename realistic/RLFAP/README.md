# Problem RLFAP
## Description
Radio Link Frequency Assignment.

## Data Example
  graph-01.json

## Model
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NValues](http://pycsp.org/documentation/constraints/NValues), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python RLFAP.py -data=<datafile.json> -variant=card
  - python RLFAP.py -data=<datafile.json> -variant=span
  - python RLFAP.py -data=<datafile.txt> -variant=max

## Links
  - https://link.springer.com/article/10.1023/A:1009812409930
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
