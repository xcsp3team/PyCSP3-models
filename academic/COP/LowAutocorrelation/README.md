# Problem LowAutocorrelation
## Description
This is the [problem 005](https://www.csplib.org/Problems/prob005/) of the CSPLib:

These problems have many practical applications in communications and electrical engineering. The objective is to
construct a binary sequence $S_i$ of length $n$ that minimizes the autocorrelations between bits. Each bit in the sequence
takes the value +1 or -1. With non-periodic (or open) boundary conditions, the k-th autocorrelation,
$C_k$ is defined to be $\Sigma_{i=0}^{n−k−1}S_i\times S_{i+k}$. With periodic (or cyclic) boundary conditions, the k-th autocorrelation,
$C_k$ is defined to be $\Sigma_{i=0}^{n−k−1}S_i \times S_{i+k mod n}$. The aim is to minimize the sum of the squares of these autocorrelations.
That is, to minimize $\Sigma_{k=1}^{n−1}$C_k^2$.





## Data
A number n, the length of the sequence.

## Model(s)


  constraints: [Intension](http://pycsp.org/documentation/constraints/Intension), [Sum](http://pycsp.org/documentation/constraints/Sum)


## Command Line

```
python LowAutocorrelation.py
python LowAutocorrelation.py -data=16
```

## Tags
 academic csplib
