"""
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

## Data Example
  words.json, mdd.json, and a number n

## Model
  constraints: Lex, MDD

## Execution
  python WordDesign2.py -data=[words.json,mdd.json,n=<number>]

## Links
  - https://www.csplib.org/Problems/prob033/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

words, transitions, n = data  # each word has 4 symbols from {C,G} and is such that its reverse and Watson-Crick complement differ in at least 4 positions
M = MDD(transitions)

# x[i][k] is the kth letter (0-A, 1-C, 2-G, 3-T) of the ith word
x = VarArray(size=[n, 8], dom=range(4))

satisfy(

    # each word must be well-formed
    [x[i] in words for i in range(n)],

    # ordering words  tag(symmetry-breaking)
    LexIncreasing(x, strict=True),

    [x[i] + x[j] in M for i, j in combinations(n, 2)]
)

""" Comments
1) For computing the Watson-Crick complement of words, we could have written:
    [(x[i][k], y[i][k]) in {(0, 3), (1, 2), (2, 1), (3, 0)} for i in range(n) for k in range(8)],

2) Is-it possible to reasoning with Cardinality constraints?
   something like [Cardinality(x[:,k], occurrences={v:range(n//4 +3) for v in range(4)}) for k in range(8)],
"""
