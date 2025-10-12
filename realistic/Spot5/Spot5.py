"""
SPOT5 earth observation satellite management problem.

The  management problems  to  be solved  can  be roughly  described as follows:
  - given a set S of photographs which can be taken the next day from at least one of the three instruments, wrt the satellite trajectory;
  - given, for each photograph, a weight expressing its importance;
  - given a set of imperative constraints: non overlapping and minimal transition time between two successive photographs on the same instrument,
   limitation on the instantaneous data flow through the satellite telemetry and on the recording capacity on board;
  - find an admissible subset S' of S (imperative  constraints set) which maximizes the sum of the weights of the photographs in S'.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2015/2022 Minizinc challenges.
The original MZN model was proposed by Simon de Givry - no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  not shown because large data files

## Model
  constraints: Sum, Table

## Execution
  python Spot5.py -data=<datafile.json>
  python Spot5.py -data=<datafile.dzn> -parser=Spot5_ParserZ.py

## Links
  - https://link.springer.com/article/10.1023/A:1026488509554
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn14, mzn15, mzn22
"""

from pycsp3 import *

assert not variant() or variant("mini")

domains, costs, c2s, c3s = data or load_json_data("0005.json")

n = len(domains)

# x[i] is the value for the ith variable
x = VarArray(size=n, dom=lambda i: domains[i])

satisfy(
    # binary constraints
    [(x[i], x[j]) in [tuple(t[i * 2:i * 2 + 2]) for i in range(len(t) // 2)] for i, j, t in c2s],

    # ternary constraints
    [(x[i], x[j], x[k]) in [tuple(t[i * 3:i * 3 + 3]) for i in range(len(t) // 3)] for i, j, k, t in c3s]
)

if not variant():
    minimize(
        costs * [x[i] == 0 for i in range(n)]
    )

elif variant("mini"):
    y = VarArray(size=n, dom={0, 1})

    satisfy(
        (y[i], x[i]) in {(0, ne(0)), (1, 0)} for i in range(n)
    )

    minimize(
        y * costs
    )

""" Comments
1) Structuring data in the associated parser makes the generation far more speeder
"""
