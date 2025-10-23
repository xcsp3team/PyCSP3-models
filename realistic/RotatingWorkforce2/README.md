# Problem: RotatingWorkforce2

Rotating workforce scheduling problem.

From the CPAIOR paper cited below: Rotating workforce scheduling is a specific personnel scheduling problem arising in many spheres of life such as, e.g., industrial plants, hospitals,
public institutions, and airline companies. A schedule must meet many constraints such as workforce requirements for shifts and days, minimal
and maximal length of shifts, and shift transition constraints.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.

## Data Example
  e025s7.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RotatingWorkforce2.py -data=<datafile.json>
  python RotatingWorkforce2.py -parser=RotatingWorkforce_Random.py <number> <number>
  python RotatingWorkforce2.py -data=<datafile.dzn> -parser=RotatingWorkforce2_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-93031-2_31
  - https://www.minizinc.org/challenge/2022/results/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  realistic, mzn22, xcsp24
