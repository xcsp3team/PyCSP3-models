# Problem: Cutstock

In the cutting stock problem, we are given items with associated lengths and demands.
We are further given stock pieces of equal length and an upper bound on the number of required stock pieces for satisfying the demand.
The objective is to minimize the number of used pieces.

## Data Example
  small.json

## Model
  constraints: [Lex](https://pycsp.org/documentation/constraints/Lex), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Cutstock.py -data=<datafile.json>
  python Cutstock.py -data=<datafile.dzn> -parser=Cutstock_ParserZ.py
```

## Links
  - https://pubsonline.informs.org/doi/10.1287/mnsc.6.4.366
  - https://link.springer.com/chapter/10.1007/978-3-540-68155-7_18
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
