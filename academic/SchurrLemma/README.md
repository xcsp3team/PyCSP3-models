# Problem: SchurrLemma

This is [Problem 015](https://www.csplib.org/Problems/prob015/) at CSPLib.

The problem is to put n balls labelled from 1 to n into 3 boxes so that for any triple of balls (x,y,z) with x+y=z,
not all are in the same box.
The variant 'mod' has been proposed by Bessiere Meseguer Freuder Larrosa, "On forward checking for non-binary constraint satisfaction", 2002.

## Example
  A solution for 5 integers to put inside 4 boxes:
  ```
    1 2 1 2 3
  ```

## Data
  A pair (n,d) where n is the number of balls, d the number of boxes

## Model
  There are two variants of this problem:
    - the first one with NValues (NotAllEqual),
    - the other one with AllDifferent

  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [NValues](https://pycsp.org/documentation/constraints/NValues)

## Execution
```
  python SchurrLemma.py -data=[number,number]
  python SchurrLemma.py -data=[number,number] -variant=mod
```

## Links
  - https://en.wikipedia.org/wiki/Schur%27s_lemma
  - https://www.sciencedirect.com/science/article/pii/S0004370202002631
  - https://www.csplib.org/Problems/prob015/

## Tags
  academic, csplib
