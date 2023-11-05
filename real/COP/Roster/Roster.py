"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
Instances (and the model) wre developed in the context of the ESPRIT PROJECT 22165 CHIC-2, with contributions from:
  - IC-Parc, Imperial College, London,
  - Bouygues research, Paris,
  - EuroDecision, Paris,
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  08.json

## Model
  constraints: Count, Sum

## Execution
  python Roster.py -data=<datafile.json>
  python Roster.py -data=<datafile.dzn> -parser=Roster_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  real, mzn09, mzn11, mzn15, mzn23
"""

from pycsp3 import *

nWeeks, requirements, lb = data
Rest, Morn, Day, Eve, Joker = shifts = range(5)
nDays, nShifts, horizon = 7, len(shifts), 7 * nWeeks

evemorn = Var(range(horizon + 1))

isolated = Var(range(horizon + 1))

# x[w][d] is the shift for day d in week w
x = VarArray(size=[nWeeks, nDays], dom=range(nShifts))

# the objective to be minimized
z = Var(dom=range(lb, 2 * horizon + 1))

x_flat = flatten(x)  # useful auxiliary array for posting some constraints

satisfy(
    # ensuring shift requirements are satisfied
    [Count(x[:, day], value=shift) == requirements[shift, day] for shift in range(nShifts) for day in range(nDays)],

    # ensuring that in any sequence of 7 days, at least one of them is a Rest day
    [Count(x_flat[d:d + 7], value=Rest) >= 1 for d in range(horizon)],

    # ensuring there is no sequence of three Rest days in a row
    [Count(x_flat[d:d + 4], value=Rest) <= 3 for d in range(horizon)],

    # counting Evenings before Mornings
    evemorn == Sum(both(x_flat[d] == Eve, x_flat[d + 1] == Morn) for d in range(horizon)),

    # counting isolated Rest days
    isolated == Sum((x_flat[d + 1] == Rest) & ~((x_flat[d] == Rest) | (x_flat[d + 2] == Rest)) for d in range(horizon)),

    # computing the objective value
    z == evemorn + isolated
)

minimize(
    z
)

"""
1) no need for x_flat_ext (longflatroster) because there is an auto-adjustment of array indexing
  x_flat_ext = x_flat + x_flat[:6]
"""
