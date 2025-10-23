# Problem: NaiveMagicSequence

This naive model for the magic sequence allows us to test the ability of solvers to handle many simple constraints at the same time.
For a problem of size 50, roughly 5000 propagators are needed.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008/2013/2015 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  An integer n

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python NaiveMagicSequence.py -data=<number>
```

## Links
  - https://www.minizinc.org/challenge/2015/results/

## Tags
  academic, mzn08, mzn13, mzn15
