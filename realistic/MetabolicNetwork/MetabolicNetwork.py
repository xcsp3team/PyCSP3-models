"""
The model, below, is close to (can be seen as the close translation of) the one (called network_50) submitted to the 2024 Minizinc challenges.
The original MZN model is accompanied with a MIT Licence (Copyright 2024 Maxime Mahout, François Fages).

## Data Example
  09.json

## Model
  constraints: Sum

## Execution
  python MetabolicNetwork.py -data=<datafile.json>
  python MetabolicNetwork.py -data=<datafile.json> -parser=MetabolicNetwork_Converter.py
  python MetabolicNetwork.py -data=<datafile.dzn> -parser=MetabolicNetwork_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2024/results/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, mzn24, xcsp25
"""

from pycsp3 import *

nReactions, stoichiometry_matrix, reversible_indicators = data or load_json_data("09.json")

iub = 50  # integer upper bound

# x[j] is the flux wrt the jth reaction
x = VarArray(size=nReactions, dom=range(iub + 1))

# z[j] is 1 if the jth reaction is done
z = VarArray(size=nReactions, dom={0, 1})

satisfy(
    # excluding trivial solution (only zeros)
    Sum(z) >= 1,

    # computing supports
    [z[j] == (x[j] > 0) for j in range(nReactions)],

    # handling steady-states
    [x * row == 0 for row in stoichiometry_matrix],

    # respecting reversibility
    [z * row <= 1 for row in reversible_indicators]
)

minimize(
    # minimizing reactions
    Sum(z)
)

""" Comments
1) use 
 [(z[j], x[j]) in [(0, 0), (1, gt(0))] for j in range(nReactions)]
 instead of the current group 'computing supports' for generating instances compatible with mini-tracks
"""
