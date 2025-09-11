# Problem: FastMatrixMultiplication

from CP'23 paper whose URL is given below:
    The multiplication of two matrices A and B of sizes n×m and m×p results in a product matrix C of size n×p.
    This operation can be represented by a binary third-order tensor T.
    An entry Ti,j,k of this tensor is equal to 1 if and only if the kth entry in the output matrix C uses the scalar product of the ith entry of A and the jth entry of B.
    The FMM (Fast Matrix Multiplication) problem for a given tensor T, rank R, and field F (e.g., F = {−1, 0, +1}) asks:
    can each entry Ti,j,k of T be expressed as the sum of exactly R trilinear terms involving the factor matrices U, V, and W, as follows:
    Ti,j,k = Σ^R_r=1 Ui,r × Vj,r × Wk,r, ∀i ∈ {1, ..., n×m}, j ∈ {1, ..., m×p}, k ∈ {1, ..., n×p}.

## Data
  four integers n, m, p, and R

## Model
  constraints: [Lex](https://pycsp.org/documentation/constraints/Lex), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python FastMatrixMultiplication.py -data=[number,number,number,number]
  python FastMatrixMultiplication.py -data=[number,number,number,number] -variant=table
```

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol280-cp2023/LIPIcs.CP.2023.14/LIPIcs.CP.2023.14.pdf
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
