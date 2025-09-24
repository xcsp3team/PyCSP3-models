# Problem: Heterosquare

From mathworld.wolfram.com:
    A heterosquare is an n×n array of the integers from 1 to n^2 such that the rows, columns, and diagonals have different sums.
    By contrast, in a magic square, they have the same sum.
    There are no heterosquares of order two, but heterosquares of every odd order exist.
    They can be constructed by placing consecutive integers in a spiral pattern.

Important: the variants of the model, below, are here for hardening the problem (when looking for a solution) ; it was written for the 2025 XCSP3 competition.

## Data
  a number n

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Heterosquare.py -data=number
  python Heterosquare.py -data=number -variant=easy
  python Heterosquare.py -data=number -variant=fair
  python Heterosquare.py -data=number -variant=hard
```

## Links
  - https://mathworld.wolfram.com/Heterosquare.html
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, xcsp25
