# Problem: CarpetCutting

The carpet cutting problem is a two-dimensional cutting and packing problem in which carpet shapes are cut
from a rectangular carpet roll with a fixed roll width and a sufficiently long roll length.
See the "Optimal Carpet Cutting" conference paper published at CP'11.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Illustration
  test01.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python CarpetCutting.py -data=test01.json
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-642-23786-7_8
  - https://www.minizinc.org/challenge/2025/results/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, mzn11, mzn12, mzn16, mzn21, mzn25, xcsp23
