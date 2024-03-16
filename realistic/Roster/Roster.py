"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
Instances (and the model) wre developed in the context of the ESPRIT PROJECT 22165 CHIC-2, with contributions from:
  - IC-Parc, Imperial College, London,
  - Bouygues research, Paris,
  - EuroDecision, Paris,
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  05.json

## Model
  constraints: Count, Sum

## Execution
  python Roster.py -data=<datafile.json>
  python Roster.py -data=<datafile.dzn> -parser=Roster_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn09, mzn11, mzn15, mzn23
"""

from pycsp3 import *

nWeeks, requirements, lb = data
REST, MORN, DAY, EVE, JOKER = shifts = range(5)
nDays, nShifts, horizon = 7, len(shifts), 7 * nWeeks

# x[w][d] is the shift for day d in week w
x = VarArray(size=[nWeeks, nDays], dom=range(nShifts))

# z1 is the number of evenings before mornings
z1 = Var(range(horizon + 1))

# z2 is the number of isolated rest days
z2 = Var(range(horizon + 1))

# the objective to be minimized
z = Var(dom=range(lb, 2 * horizon + 1))

x_flat = flatten(x)  # useful auxiliary array for posting some constraints

satisfy(
    # ensuring shift requirements are satisfied
    [Count(x[:, day], value=shift) == requirements[shift, day] for shift in range(nShifts) for day in range(nDays)],

    # ensuring that in any sequence of 7 days, at least one of them is a Rest day
    [Count(x_flat[d:d + 7], value=REST) >= 1 for d in range(horizon)],

    # ensuring there is no sequence of three Rest days in a row
    [Count(x_flat[d:d + 4], value=REST) <= 3 for d in range(horizon)],

    # counting Evenings before Mornings
    z1 == Sum(
        both(
            x_flat[d] == EVE,
            x_flat[d + 1] == MORN
        ) for d in range(horizon)
    ),

    # counting isolated Rest days
    z2 == Sum(
        conjunction(
            x_flat[d] != REST,
            x_flat[d + 1] == REST,
            x_flat[d + 2] != REST
        ) for d in range(horizon)
    ),

    # computing the objective value
    z == z1 + z2
)

minimize(
    z
)

"""
1) no need for x_flat_ext (longflatroster) because there is an auto-adjustment of array indexing
  x_flat_ext = x_flat + x_flat[:6]
"""
