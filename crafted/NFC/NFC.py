"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2022 challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  12-2-05.json

## Model
  constraints: Flow, Sum

## Execution
  python NFC.py -data=<datafile.json>
  python NFC.py -data=<datafile.dzn> -parser=NFC_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  crafted, mzn16, mzn22
"""

from pycsp3 import *

shift, workers = data or load_json_data("12-2-05.json")

nPeriods = len(workers)
P = range(nPeriods)

A = [(i, (i + 1) % nPeriods) for i in P] + [(i, (i + nPeriods - shift) % nPeriods) for i in P]

# w[i] is the number of workers at the ith period
w = VarArray(size=nPeriods, dom=range(max(workers) + 1))

f = VarArray(size=nPeriods, dom=range(max(workers) + 1))

# z is the cost of the flow
z = Var(dom=range(nPeriods * max(workers) + 1))

satisfy(
    # ensuring a minimum number of workers at each period
    [w[i] >= workers[i] for i in P],

    # computing the cost of the flow
    Flow(
        w + f,
        balance=0,
        arcs=A,
        weights=[1] * nPeriods + [0] * nPeriods
    ) == z,

    [w[i] == Sum(f[i + 1:i + 1 + shift]) for i in P]
)

minimize(
    # minimizing the cost of the flow
    z
)

""" Comments
1) Note that:
 Sum(f[i + 1:i + 1 + shift])
   is equivalent to:
 Sum(f[(i + k) % nPeriods] for k in range(1, shift + 1)) 
Here, automatic index auto-adjustment is used
"""
