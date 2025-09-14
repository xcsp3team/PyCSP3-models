"""
The model, below, is close to (can be seen as the close translation of) the one (called network_50) submitted to the 2024 Minizinc challenges.
Original model with MIT Licence (Copyright 2024 Maxime Mahout, François Fages).

## Data Example
  09.json

## Model
  constraints: Sum

## Execution
  python MetabolicNetwork.py -data=<datafile.json>
  python MetabolicNetwork.py -data=<datafile.json> -parser=MetabolicNetwork_Converter.py
  python MetabolicNetwork.py -data=<datafile.dzn> -parser=MetabolicNetwork_ParserZ.py

## Links
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop
  - https://www.minizinc.org/challenge2014/results2024.html

## Tags
  realistic, mzn24, xcsp25
"""

from pycsp3 import *

nReactions, stoichiometry_matrix, reversible_indicators = data
nMetabolites, nReversibleReactions = len(stoichiometry_matrix), len(reversible_indicators)

iub = 50  # integer upper bound

# x[j] is the flux wrt the jth reaction
x = VarArray(size=nReactions, dom=range(iub + 1))

# z[j] is 1 if the jth reaction is done
z = VarArray(size=nReactions, dom={0, 1})

satisfy(
    # excluding trivial solution (only zeros)
    Sum(z) >= 1,

    # computing supports
    [z[j] == (x[j] > 0) for j in range(nReactions)] if not variant()
    else [(z[j], x[j]) in [(0, 0), (1, gt(0))] for j in range(nReactions)],  # for mini-tracks

    # handling steady-states
    [x * stoichiometry_matrix[i] == 0 for i in range(nMetabolites)],

    # respecting reversibilities
    [z * reversible_indicators[i] <= 1 for i in range(nReversibleReactions)]
)

minimize(
    # minimizing reactions
    Sum(z)
)

"""
1) use -variant=mini for generating instances compatible with mini-tracks
"""
