# Problem: EFPA

 Proposed by Peter Nightingale at CSPLib:
     "The problem is to find a set (optionally of maximal size) of codewords, such that any pair of codewords are Hamming distance d apart.
     Each codeword is made up of symbols from the alphabet {1,…,q}, with each symbol occurring a fixed number λ of times per codeword."

## Data
four numbers d, ld, q and n

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Count](https://pycsp.org/documentation/constraints/Count), [Lex](https://pycsp.org/documentation/constraints/Lex)

## Execution
```
  python EFPA.py -data=[number,number,number,number]
```

## Links
  - https://www.csplib.org/Problems/prob055/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, csplib, xcsp25
