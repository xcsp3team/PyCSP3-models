# Problem: DeBruijn

In combinatorial mathematics, a de Bruijn sequence of order n on an alphabet A of size b is a cyclic sequence
in which every possible length-n string on A occurs exactly once as a substring.

## Data
  A pair (b,n) of integer values, the value of n and the size of the alphabet.

### Example
  For n=2 and an alphabet {a,b,c}, a sequence is
  ```
     a a c b b c c a b
  ```

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Debruijn.py -data=[number,number]
```

## Links
  - https://en.wikipedia.org/wiki/De_Bruijn_sequence
  - https://mathworld.wolfram.com/deBruijnSequence.html
  - http://www.hakank.org/common_cp_models/#debruijn
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, mzn08
