# Problem WordDesign
## Description
This is the [problem 033](https://www.csplib.org/Problems/prob033/) of the CSPLib:

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
TODO
A number n, the number of integer.
## Model(s)
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [LexIncreasing](http://pycsp.org/documentation/constraints/LexIncreasing)

## Command Line
```
python WordDesign -data=[WordDesign.json,n=10]
```

## Tags
 academic
