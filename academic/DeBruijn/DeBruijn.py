"""
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
  constraints: AllDifferent, Cardinality, Minimum, Sum

## Execution
  python Debruijn.py -data=[number,number]

## Links
  - https://en.wikipedia.org/wiki/De_Bruijn_sequence
  - https://mathworld.wolfram.com/deBruijnSequence.html
  - http://www.hakank.org/common_cp_models/#debruijn
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, mzn08
"""

from pycsp3 import *

b, n = data
m = b ** n
powers = [b ** i for i in range(n - 1, -1, -1)]

# x[i] is the ith number (in base 10) of the sequence
x = VarArray(size=m, dom=range(m))

# d[i][j] is the jth digit in base b for the ith number of the sequence
d = VarArray(size=[m, n], dom=range(b))

# g[i] is the number of occurrences of digit i in the first column of array d
g = VarArray(size=b, dom=range(m + 1))

satisfy(
    # ensuring all numbers are different
    AllDifferent(x),

    # ensuring d[i] is the representation of x[i] in base b
    [d[i] * powers == x[i] for i in range(m)],

    # imposing de Bruijn condition
    [d[i - 1][j] == d[i % m][j - 1] for i in range(1, m + 1) for j in range(1, n)],

    # computing occurrences
    Cardinality(
        within=d[:, 0],
        occurrences=g
    ),

    # imposing the first element as the smallest element
    # tag(symmetry-breaking)
    x[0] == Minimum(x)
)

""" Comments
1) data used in Challenge 2008 are: (2,3), (2,7), (2,8), (2,9), (2,10), (3,6), (3,7), (3,8), (4,6), (4,7), (4,8)
"""
