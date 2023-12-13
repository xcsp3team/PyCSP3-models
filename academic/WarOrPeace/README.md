# Problem WarOrPeace
## Description
There are n countries.
Each pair of two countries is either at war or has a peace treaty.
Each pair of two countries that has a common enemy has a peace treaty.
What is the minimum number of peace treaties?

The minimum number of peace treaties for n in [2..12] seems to be floor(n^2/4), see https://oeis.org/A002620
Hence, it is 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81, ...

## Data
  an integer n

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python WarOrPeace.py -data=number
  - python WarOrPeace.py -data=number -variant=or

## Links
  - https://oeis.org/A002620
  - http://www.hakank.org/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  academic, xcsp22
