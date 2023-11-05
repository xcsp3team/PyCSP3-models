# Problem CarpetCutting
## Description
The carpet cutting problem is a two-dimensional cutting and packing problem in which carpet shapes are cut
from a rectangular carpet roll with a fixed roll width and a sufficiently long roll length.
See the "Optimal Carpet Cutting" conference paper published at CP'11.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  test01.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  python CarpetCutting.py -data=test01.json

## Links
  - https://link.springer.com/chapter/10.1007/978-3-642-23786-7_8
  - https://www.minizinc.org/challenge2021/results2021.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, mzn11, mzn12, mzn16, mzn21, xcsp23
