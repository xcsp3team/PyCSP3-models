# Problem: Hamming

Given four integers n, m, d and k, the goal is to find n vectors of size m where each value lies between 0 and d (exclusive),
and every two vectors have a Hamming distance at most equal to k

## Data
  four integers n, m, d, and k

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Lex](https://pycsp.org/documentation/constraints/Lex)

## Execution
```
  python Hamming.py -data=[number,number,number,number]
  python Hamming.py -data=[number,number,number,number] -variant=mini
```

## Links
  - https://en.wikipedia.org/wiki/Hamming_distance
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
