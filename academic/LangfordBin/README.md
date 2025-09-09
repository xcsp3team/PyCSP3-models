# Problem: LangfordBin

From paper (by Gent, Jefferson and Miguel at CP'06]:
    Langford’s Problem L(k, n) requires ﬁnding a list of length k∗n, which contains k sets of the numbers 1 to n,
    such that for all m ∈ {1, 2, ..., n} there is a gap of size m between adjacent occurrences of m.
    In the constraint solver Minion, L(2,n) was modelled using two vectors of variables, V and P, each of size 2n.
    Each variable in V has domain {1, 2, ..., n}, and V represents the result.
    For each i ∈ {1, 2, ...} the 2ith and 2i + 1st variables in P are the ﬁrst and second positions of i in V.
    Each variable in P has domain {0, 1, ..., 2n−1}, indexing matrices from 0.

## Data
  An integer n

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element)

## Execution:
```
  python LangfordBin.py -data=number
```

## Links
  - https://link.springer.com/chapter/10.1007/11889205_15
  - https://www.csplib.org/Problems/prob024/

## Tags
  academic, csplib, xcsp25
