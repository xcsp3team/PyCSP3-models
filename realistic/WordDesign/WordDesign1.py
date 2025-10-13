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
  words.json, and a number n

## Model
  constraints: Lex, Sum, Table

## Execution
  python WordDesign1.py -data=[words.json,n=<number>]

## Links
  - https://www.csplib.org/Problems/prob033/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

words, n = data or (load_json_data("words.json"), 25)

m = 8  # size of the words

N, M = range(n), range(m)

# x[i][j] is the jth letter (0-A, 1-C, 2-G, 3-T) of the ith word
x = VarArray(size=[n, m], dom=range(4))

# y[i][j] is the jth letter of the Watson-Crick complement of the ith word (in x)
y = VarArray(size=[n, m], dom=range(4))

satisfy(
    # computing the Watson-Crick complement of words
    [x[i][j] + y[i][j] == 3 for i in N for j in M],

    # each word must be well-formed
    [x[i] in words for i in N],

    # ordering words  tag(symmetry-breaking)
    LexIncreasing(x, strict=True),

    # each pair of distinct words differ in at least 4 positions
    [
        Sum(
            x[i1][j] != x[i2][j] for j in M
        ) >= 4 for i1, i2 in combinations(N, 2)
    ],

    # each pair of distinct words are such that the reverse of the former and the Watson-Crick complement of the latter differ in at least 4 positions
    [
        Sum(
            x[i1][7 - j] != y[i2][j] for j in M
        ) >= 4 for i1 in N for i2 in N if i1 != i2
    ]
)

""" Comments
1) For computing the Watson-Crick complement of words, we could have written:
   [(x[i][j], y[i][j]) in {(0, 3), (1, 2), (2, 1), (3, 0)} for i in N for j in M],

2) The second parameter n is given independently of the JSON file

3) Data used for the 2023 competition are: [5, 15, 25, 35, 45, 55, 65, 75, 85, 100]
   together with the file "words.json"
   
4) Each word in words.json has 8 symbols from {C,G} and is such that its reverse and Watson-Crick complement differ in at least 4 positions
"""
