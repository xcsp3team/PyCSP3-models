"""
CELAR radio link frequency assignment problem.

The Radio Link Frequency Assignment Problem (RLFAP) consists in assigning frequencies to communication links
in such a way that no interferences  occurs.
In the simplest case which is considered here, only two types of constraint occur:
  1 the absolute difference between two frequencies should be greater than a given number k (|x-y|>k)
  2 the absolute difference between two frequencies should exactly be equal to a given number k (|x-y|=k)
If there is no solution, (1) become soft constraints while (2) remain hard constraints,
and you have to minimize a weighted sum of the violated soft constraints.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2016 Minizinc challenges.
The MZN model was proposed by Simon de Givry.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  graph11.json

## Model
  constraints: Sum, Table

## Execution
  python Celar.py -data=<datafile.json>
  python Celar.py -data=<datafile.dzn> -parser=Celar_ParserZ.py

## Links
  - https://link.springer.com/article/10.1023/A:1009812409930
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  real, mzn13, mzn16
"""

from pycsp3 import *

domainTypes, domains, minFreq, maxFreq, hards, softs, costs = data
n = len(domains)

# x[i] is the frequency used for the ith antenna
x = VarArray(size=n, dom=range(minFreq, maxFreq + 1))

satisfy(
    # each variable takes a value from its domain
    [x[i] in domainTypes[domains[i]] for i in range(n)],

    # hard equality constraints
    [abs(x[i] - x[j]) == k for (i, j, k) in hards]
)

minimize(
    # minimizing penalty costs
    Sum(costs[w] * (abs(x[i] - x[j]) <= k) for (w, i, j, k) in softs)
)
