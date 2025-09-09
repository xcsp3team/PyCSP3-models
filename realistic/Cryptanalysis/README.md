# Problem: Cryptanalysis

Chosen Key Differential Cryptanalysis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 Minizinc challenge.
The MZN model was proposed by David Gerault, Marine Minier, and Christine Solnon.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integers

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Cryptanalysis.py -data=<n,z,k>
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-44953-1_37
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn16, xcsp25
