# Problem: Cryptanalysis

Chosen Key Differential Cryptanalysis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 Minizinc challenge.
The original MZN model was proposed by David Gerault, Marine Minier, and Christine Solnon - no licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integers: n, z and k

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Cryptanalysis.py -data=[number,number,number]
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-44953-1_37
  - https://www.minizinc.org/challenge/2016/results/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  realistic, mzn16, xcsp25
