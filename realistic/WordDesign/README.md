# Problem WordDesign

See Problem 033 on CSPLib.

The problem is to find as large as possible a set S of strings (words) of length 8
over the alphabet W = { A,C,G,T } with the following properties:
 - each word in S has 4 symbols from { C,G }
 - each pair of distinct words in S differ in at least 4 positions
 - each pair of words x and y in S (where x and y may be identical) are such that
   xR and yC differ in at least 4 positions. Here, (x1,...,x8 )R = (x8,...,x1) is
   the reverse of (x1,...,x8) and (x1,...,x8)C is the Watson-Crick complement of
   (x1,...,x8), i.e. the word where each A is replaced by a T and vice versa
   and each C is replaced by a G and vice versa.

This problem has its roots in Bioinformatics and Coding Theory.

## Data
  words.json, and a number n

## Model
  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python WordDesign1.py -data=[words.json,n=<number>]
```

## Links
  - https://www.csplib.org/Problems/prob033/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  realistic, xcsp23
