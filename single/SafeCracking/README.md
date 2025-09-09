# Problem: SafeCracking

From the Oz Primer.

The code of Professor Smart's safe is a sequence of 9 distinct
nonzero digits d1 .. d9 such that the following equations and
inequations are satisfied:
```
       d4 - d6   =   d7
  d1 * d2 * d3   =   d8 + d9
  d2 + d3 + d6   <   d8
            d9   <   d8
  d1 <> 1, d2 <> 2, ..., d9 <> 9
```
Can you find the correct combination?

## Data
  all integrated (single problem)

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent)

## Execution
```
  python SafeCracking.py
```

## Links
 -  http://www.comp.nus.edu.sg/~henz/projects/puzzles/digits/index.html

## Tags
  single
