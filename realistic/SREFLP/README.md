# Problem: SREFLP

The Single-Row Facility Layout Problem (SRFLP) is an ordering problem considering a set of departments in a facility,
with given lengths and pairwise traffic intensities.
Its goal is to find a linear ordering of the departments minimizing the weighted sum of the distances between department pairs.
See CP paper below.

## Data Example
  Cl07.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python SREFLP.py -data=<datafile.json>
  python SREFLP.py -data=<datafile.txt> -parser=SREFLP_Parser.py
```

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol235-cp2022/LIPIcs.CP.2022.14/LIPIcs.CP.2022.14.pdf
  - https://github.com/vcoppe/csrflp-dd
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
