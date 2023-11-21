"""

You can see below, the beginning of the description provided by [Wolfram Mathworld](https://mathworld.wolfram.com/deBruijnSequence.html):

"*The shortest circular sequence of length $\sigma^n$ such that every string of length $n$
on the alphabet $a$ of size $\sigma$ occurs as a contiguous subrange of the sequence described by $a$.*"



### Example

For n=2 and an alphabet (a,b,c), a sequence is
```
     a a c b b c c a b
```


## Data
a couple \[n,|a|], the value of n and the size of the alphabet.

## Model(s)

constraints: AllDifferent, Sum, Intension, Cardinality, Minimum

## Command Line

python DeBruijnSequence.py
python DeBruijnSequence.py -data=[2,5]

## Tags
 academic
"""

from pycsp3 import *

b, n = data or (3, 4)
m = b ** n
powers = [b ** i for i in range(n - 1, -1, -1)]

# x[i] is the ith number (in base 10) of the sequence
x = VarArray(size=m, dom=range(m))

# d[i][j] is the jth digit in the base for the ith number of the sequence; d[i] is then the representation in the base of the ith number
d = VarArray(size=[m, n], dom=range(b))

# g[i] is the number of occurrences of digit i in the first column of array d
g = VarArray(size=b, dom=range(m + 1))

satisfy(
    AllDifferent(x),

    # linking x and d: d[i] is the representation of x[i] in base 2
    [d[i] * powers == x[i] for i in range(m)],

    # de Bruijn condition
    [d[i - 1][j] == d[i % m][j - 1] for i in range(1, m + 1) for j in range(1, n)],

    Cardinality(d[:, 0], occurrences={i: g[i] for i in range(b)}),

    # tag(symmetry-breaking)
    Minimum(x) == x[0]
)
