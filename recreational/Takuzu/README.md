# Problem: Takuzu

From Wikipedia:
    Takuzu, also known as Binairo, is a logic puzzle involving placement of two symbols, often 1s and 0s, on a rectangular grid.
    The objective is to fill the grid with 1s and 0s, where there is an equal number of 1s and 0s in each row and column and no more than two of either number adjacent to each other.
    Additionally, there can be no identical rows or columns.

## Data
  an integer n, and clues (possibly None)

## Model
  constraints: [AllDifferentList](https://pycsp.org/documentation/constraints/AllDifferentList), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Takuzu.py -data=<datafile.json>
  python Takuzu.py -data=[number,None]
  python Takuzu.py -data=<datafile.json> -variant=mini
```

## Links
  - https://en.wikipedia.org/wiki/Takuzu
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, recreational, xcsp24
