"""
Weighted multi-set cover.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist.
The model and the instances are extracted from an industrial use-case.
MIT License.

## Data
  b0-c115-i0-small-subset-e3-sr1295-cd41.json

## Model
  constraints: Sum

## Execution
  python WMSC.py -data=b0_c115_i1_base_full_e3_sr702_cd86.json
  python WMSC.py -data=b0_c115_i1_base_full_e3_sr702_cd86.dzn -dataparser=WMSC_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn21
"""

from pycsp3 import *

requirements, candidateSets, candidateWeights = data
n, m = len(requirements), len(candidateSets)

# x[i] is the number of times a candidate is used
x = VarArray(size=m, dom=range(max(requirements) + 1))

satisfy(
    # a cover is needed
    requirements[e] <= candidateSets[:, e] * x for e in range(n)
)

minimize(
    # minimizing the sum of weighted used candidates
    candidateWeights * x
)
