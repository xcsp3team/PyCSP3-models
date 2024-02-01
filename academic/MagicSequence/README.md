# Problem MagicSequence

This is [Problem 019](https://www.csplib.org/Problems/prob019/) at CSPLib.

A magic sequence of length n is a sequence of integers x between 0 and n−1, such that for all i in 0 to n−1,
the number i occurs exactly x[i] times in the sequence.


## Data
  An integer n, the size of the sequence.

## Example
  A magic sequence for n=10.
  ```
    6 2 1 0 0 0 1 0 0 0
  ```

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/MagicSequence/).

  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MagicSequence.py -data=number
```

## Tags
 academic, notebook, csplib
