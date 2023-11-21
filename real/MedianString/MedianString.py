"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  p1-15-20-1.json

## Model
  constraints: Sum

## Execution
  python MedianString.py -data=<datafile.json>
  python MedianString.py -data=<datafile.dzn> -parser=MedianString_ParserZ.py

## Links
  - https://ojs.aaai.org/index.php/AAAI/article/view/5530
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn19
"""

from pycsp3 import *

maxLength, medLength, maxChar, strings = data
nStrings = len(strings)

pairs = [(i, j) for i in range(nStrings) for j in range(1, maxLength + 1)]

# x[i] is the ith character of the median string
x = VarArray(size=maxLength, dom=range(maxChar + 1))

# z[i] is the global edit distance between the ith string and the set of strings
z = VarArray(size=nStrings, dom=range(2 * maxLength + 1))

# t[i][j][k] is the distance between the ith string and the median after considering j and k characters
t = VarArray(size=[nStrings, maxLength + 1, maxLength + 1], dom=range(maxLength * 2 + 1))

satisfy(
    # at the beginning, the distance is 0
    t[:, 0, 0] == 0,

    # at the end, the global distance is computed
    t[:, -1, -1] == z,

    # upper bound on gradually computed distances
    [t[i][j][k] <= j + k for i, j in pairs for k in range(1, maxLength + 1)],

    # setting distances when first characters
    [
        [t[i][0][k] == k for i, k in pairs],
        [t[i][j][0] == j for i, j in pairs]
    ],

    # iterative computation
    [
        t[i][j][k] == ift(
            x[k - 1] == strings[i][j - 1],
            Then=t[i][j - 1][k - 1],
            Else=ift(
                x[k - 1] == 0,
                Then=t[i][j][k - 1],
                Else=(t[i][j - 1][k] if strings[i][j - 1] == 0 else min(t[i][j - 1][k] + 1, t[i][j][k - 1] + 1))
            )
        ) for i, j in pairs for k in range(1, maxLength + 1)
    ],

    # ensuring the median is 0 after its length
    [x[i] == 0 for i in range(medLength, maxLength)]
)

minimize(
    # minimizing the global edit distance
    Sum(z)
)

"""
1) using hybrid tables?
2) note that:
 t[:, -1, -1] == z
   is a shortcut for:
 [t[i][-1][-1] == z[i] for i in range(nStrings)]

"""
