"""
 Proposed by Peter Nightingale at CSPLib:
     "The problem is to find a set (optionally of maximal size) of codewords, such that any pair of codewords are Hamming distance d apart.
     Each codeword is made up of symbols from the alphabet {1,…,q}, with each symbol occurring a fixed number λ of times per codeword."

## Data
four numbers d, ld, q and n

## Model
  constraints: Cardinality, Count, Lex

## Execution
  python EFPA.py -data=[number,number,number,number]

## Links
  - https://www.csplib.org/Problems/prob055/

## Tags
  academic, csplib, xcsp25
"""

from pycsp3 import *

t = [(3, 7, 7, 6), (3, 7, 7, 7), (3, 8, 8, 7), (3, 8, 8, 8), (3, 9, 9, 8), (3, 9, 9, 9), (4, 3, 4, 6), (4, 3, 4, 7), (4, 4, 3, 7), (4, 4, 3, 8), (4, 4, 4, 8),
     (4, 4, 4, 9), (4, 4, 5, 10), (4, 4, 5, 11), (4, 5, 4, 10), (4, 5, 4, 11), (5, 4, 3, 7), (5, 4, 3, 8), (5, 4, 4, 8), (5, 4, 4, 9), (6, 4, 3, 12),
     (6, 4, 3, 13), (6, 4, 4, 13), (6, 4, 4, 14)]
d, ld, q, n = t[data] if isinstance(data, int) else data

# x[i] is the ith symbol of the sequence
x = VarArray(size=[n, q * ld], dom=range(q))

satisfy(
    # respecting the occurrences of symbols
    [Cardinality(x[i], occurrences={j: ld for j in range(q)}) for i in range(n)],

    # ensuring a specific Hamming distance
    [Hamming(x[i], x[j]) == d for i, j in combinations(n, 2)],

    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)  # strict not possible (except maybe for the rows)
)

Compilation.string_data = "-" + "-".join(str(v) for v in (d, ld, q, "{:02d}".format(n)))

"""
1) Data used for the 205 competition are: [0, 1, 2, 3, 12, 13, 14, 15, 18, 19, 22, 23]
"""

# Precedence(x[0]),
