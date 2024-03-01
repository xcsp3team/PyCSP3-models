# Problem GolombRuler

This is [Problem 006](https://www.csplib.org/Problems/prob006/) at CSPLib.

A Golomb ruler is defined as a set of n integers v1 < v2 < ... < vn such that the n x (n-1)/2 differences vj - vi are distinct.
Such a ruler is said to contain n marks (or ticks) and to be of length vn.
The objective is to find optimal rulers (i.e., rulers of minimum length).

An optimal Golomb ruler with 4 ticks.
<small>Image from [commons.wikimedia.org](https://commons.wikimedia.org/wiki/File:Golomb_Ruler-4.svg) </small>
<img src="https://pycsp.org/assets/notebooks/figures/golomb.png" alt="Golomb ruler" width="300" />

This problem (and its variants) is said to have many practical applications including sensor placements for x-ray crystallography and radio astronomy.

### Example
  The optimum for n=8
  ```
     0  1  4  9  15  22  32  34
  ```

## Data
  A number n, the number of integers.

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/GolombRuler/).

  Here, there are 3 variants:
    - a main one
    - a variant "dec" by decomposing the AllDifferent constraint
    - a variant "aux" with auxiliary variables

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Maximum](http://pycsp.org/documentation/constraints/Maximum)

## Execution
  - python GolombRuler.py -data=number
  - python GolombRuler.py -data=number -variant=dec
  - python GolombRuler.py -data=number -variant=aux

## Links
  - https://www.csplib.org/Problems/prob006/

## Tags
  academic, notebook, csplib
