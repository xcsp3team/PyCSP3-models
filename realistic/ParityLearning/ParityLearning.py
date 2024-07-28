"""
Optimization variant of the minimal disagreement parity (MDP) problem.

The MDP problem is introduced in the paper whose link is given below.
Given a set of sample input vectors and a set of sample parities, one has to
find the bits of the input vectors on which the parities were computed.
While the original problem is a satisfaction problem, in this variant,
one wants a solution that minimizes the number of errors.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  44-22-5-2.json

## Model
  constraints: Sum

## Execution
  python ParityLearning.py -data=<datafile.json>
  python ParityLearning.py -data=<datafile.dzn> -parser=ParityLearning_ParserZ.py

## Links
  - https://www.cis.upenn.edu/~mkearns/papers/CrawfordKearnsSchapire.pdf
  - https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/DIMACS/PARITY/descr.html
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
"""

from pycsp3 import *

maxErrors, sampleOutputs, sampleInputs = data
m, n = len(sampleOutputs), len(sampleInputs[0])  # m is the number of samples, n is the number of variables

assert 0 <= maxErrors <= m and n > 0 and m > 0

# x[i] is the ith parity bit
x = VarArray(size=n, dom={0, 1})

# y[j] is the computed parity for the jth sample
y = VarArray(size=m, dom={0, 1})

# z is the number of errors
z = Var(dom=range(maxErrors + 1))

satisfy(
    # computing the parity of samples
    [
        y[j] == xor(
            x[i] for i in range(n) if sampleInputs[j][i]
        ) for j in range(m)
    ],

    # computing the number of errors
    z == Sum(
        sampleOutputs[j] != y[j] for j in range(m)
    )
)

minimize(
    z
)
