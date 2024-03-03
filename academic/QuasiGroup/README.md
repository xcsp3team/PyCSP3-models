# Problem QuasiGroup

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

  constraints: [Element](http://pycsp.org/documentation/constraints/Element)

## Execution
  - python QuasiGroup.py -variant=base-v3 -data=number
  - python QuasiGroup.py -variant=base-v4 -data=number
  - python QuasiGroup.py -variant=base-v5 -data=number
  - python QuasiGroup.py -variant=base-v6 -data=number
  - python QuasiGroup.py -variant=base-v7 -data=number
  - python QuasiGroup.py -variant=aux-v3 -data=number
  - python QuasiGroup.py -variant=aux-v4 -data=number
  - python QuasiGroup.py -variant=aux-v5 -data=number
  - python QuasiGroup.py -variant=aux-v7 -data=number

## Links
  - https://www.csplib.org/Problems/prob003/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, notebook, csplib, xcsp22

<br />

## _Alternative Model(s)_

#### QuasiGroup_z.py
 - constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element)
 - tags: academic, csplib, mzn08
