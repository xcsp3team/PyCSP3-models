# Problem Magic Sequence

## Description
This is the [problem 019](https://www.csplib.org/Problems/prob019/) of the CSPLib:

"*A magic sequence of length n is a sequence of integers $x_0...x_{n−1}$ between 0 and n−1, such that for all i in 0 to n−1, 
the number i occurs exactly $x_i$ times in the sequence.*"

### Example

A magic sequence for n=10.
```
6 2 1 0 0 0 1 0 0 0 
```

## Data
A number n, the size of the sequence.

## Model(s)


You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/MagicSequence/).

*Involved Constraints*: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality/), [Sum](https://pycsp.org/documentation/constraints/Sum/).



## Command Line


```shell
  python MagicSequence.py
  python MagicSequence.py -data=10
 ```

## Some Results

| Data | Number of Solutions |
|------|---------------------|
| 8    | 1                   |
| 10   | 1                   |
| 12   | 1                   |
