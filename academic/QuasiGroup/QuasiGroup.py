"""
This is [Problem 003](https://www.csplib.org/Problems/prob003/) at CSPLib.

An order n quasigroup is a Latin square of size n.
That is, an n×n multiplication table in which each element occurs once in every row and column.
A quasigroup can be specified by a set and a binary multiplication operator, ∗ defined over this set.
Quasigroup existence problems determine the existence or non-existence of quasigroups of
a given size with additional properties. For example:
  - QG3: quasigroups for which (a ∗ b) ∗ (b ∗ a) = a
  - QG5: quasigroups for which ((b ∗ a) ∗ b) ∗ b = a
  - QG6: quasigroups for which (a ∗ b) ∗ b = a ∗ (a ∗ b)
For each of these problems, we may additionally demand that the quasigroup is idempotent.
That is, a ∗ a = a for every element a.

## Data
  A unique integer, the order of the problem instance

## Example
  ```
    1    2   3   4
    4    1   2   3
    3    4   1   2
    2    3   4   1
  ```

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Quasigroup/).

  constraints: Element

## Execution
  python QuasiGroup.py -variant=base-v3 -data=number
  python QuasiGroup.py -variant=base-v4 -data=number
  python QuasiGroup.py -variant=base-v5 -data=number
  python QuasiGroup.py -variant=base-v6 -data=number
  python QuasiGroup.py -variant=base-v7 -data=number
  python QuasiGroup.py -variant=aux-v3 -data=number
  python QuasiGroup.py -variant=aux-v4 -data=number
  python QuasiGroup.py -variant=aux-v5 -data=number
  python QuasiGroup.py -variant=aux-v7 -data=number

## Links
  - https://www.csplib.org/Problems/prob003/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, notebook, csplib, xcsp22
"""

from pycsp3 import *

BASE, AUX, V3, V4, V5, V6, V7 = "base", "aux", "v3", "v4", "v5", "v6", "v7"
assert variant() in (BASE, AUX) and subvariant() in (V3, V4, V5, V6, V7)

n = data or 8

# x[i][j] is the value at row i and column j of the quasi-group
x = VarArray(size=[n, n], dom=range(n))

# y[i][j] is the value of the auxiliary variable for row i and column j
y = VarArray(size=[n, n], dom=range(n * n if subvariant() in (V3, V4) else n)) if variant(AUX) else None


def main_property(i, j):
    if variant(BASE):
        if subvariant(V3):
            return x[x[i][j], x[j][i]] == i
        if subvariant(V4):
            return x[x[j][i], x[i][j]] == i
        if subvariant(V5):
            return x[x[x[j][i], j], j] == i
        if subvariant(V6):
            return x[x[i][j], j] == x[i, x[i][j]]
        if subvariant(V7):
            return x[x[j][i], j] == x[i, x[j][i]]
    else:  # variant AUX
        if subvariant(V3):
            return x[y[i][j]] == i, y[i][j] == x[i][j] * n + x[j][i]
        if subvariant(V4):
            return x[y[i][j]] == i, y[i][j] == x[j][i] * n + x[i][j]
        if subvariant(V5):
            return x[:, i][x[i][j]] == y[i][j], x[:, i][y[i][j]] == j
        if subvariant(V7):
            return x[:, j][x[j][i]] == y[i][j], x[i][x[j][i]] == y[i][j]
    assert False, "Should not be reached"


satisfy(
    # ensuring a Latin square
    AllDifferent(x, matrix=True),

    # ensuring idempotence  tag(idempotence)
    [x[i][i] == i for i in range(n)],

    # ensuring main property
    [main_property(i, j) for i in range(n) for j in range(n) if not (variant(AUX) and i == j)]
)
