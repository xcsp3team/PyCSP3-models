"""
See "The First Evaluation of Pseudo-Boolean Solvers (PB'05)" by Vasco M. Manquinho and Olivier Roussel. J. Satisf. Boolean Model. Comput. 2(1-4): 103-143 (2006)

## Data

## Model
  constraints: Sum

## Execution
  python PseudoBoolean.py -data=<datafile.opb> -parser=PseudoBoolean_Parser.py

## Links
  - http://www.cril.univ-artois.fr/PB16/

## Tags
  recreational
"""

from pycsp3 import *

n, e, constraints, objective = data  # n and e respectively denote the numbers of variables and constraints

x = VarArray(size=n, dom={0, 1})

satisfy(
    # respecting each linear constraint
    Sum(x[nums] * coeffs, condition=(op, limit)) for (coeffs, nums, op, limit) in constraints
)

if objective:
    minimize(
        # minimizing the linear objective
        x[objective.nums] * objective.coeffs
    )

""" Comments
1) Note that this is a very rare occasion where we need to use the named argument 'condition'.
2) Note that  
 x[objective.nums]
   is equivalent to:
 [x[i] for i in objective.nums]
"""
