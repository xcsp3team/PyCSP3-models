# Problem GolombRuler
## Description
This is the [problem 006](https://www.csplib.org/Problems/prob006/) of the CSPLib:


A Golomb ruler is defined as a set of $n$ integers $0 = a_1 < a_2 < ... < a_n$ such that the $n \times (n-1)/2$ differences $a_j - a_i$, $1 \leq i < j \leq n$, are distinct.
Such a ruler is said to contain $n$ marks (or ticks) and to be of length $a_n$.
The objective is to find optimal rulers (i.e., rulers of minimum length).

An optimal Golomb ruler with 4 ticks. <small>Image from [commons.wikimedia.org](https://commons.wikimedia.org/wiki/File:Golomb_Ruler-4.svg) </small>
<img src="https://pycsp.org/assets/notebooks/figures/golomb.png" alt="Golomb ruler" width="300" />

This problem (and its variants) is said to have many practical applications including sensor placements for x-ray crystallography and radio astronomy.


### Example

The optimum for n=8

```
    0  1  4  9  15  22  32  34
```


## Data
A number n, the number of integers.

## Model(s)
You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/GolombRuler/).

There are 3 variants:
 - one with all different constraint based on expression
 - one with auxilliary variables
 - and one with  intension constraints.

  constraints: [Intension](http://pycsp.org/documentation/constraints/Intension), [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent)


## Command Line


```
python GolombRuler.py
python GolombRuler.py -data=10
python GolombRuler.py -data=10 -variant=dec
python GolombRuler.py -data=10 -variant=aux
```

## Tags
 academic

