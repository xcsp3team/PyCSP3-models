"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
Instances (and the model) wre developed in the context of the ESPRIT PROJECT 22165 CHIC-2, with contributions from:
  - IC-Parc, Imperial College, London
  - Bouygues research, Paris
  - EuroDecision, Paris
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  05.json

## Model
  constraints: Count, Sum

## Execution
  python Roster.py -data=<datafile.json>
  python Roster.py -data=<datafile.dzn> -parser=Roster_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn09, mzn11, mzn15, mzn23
"""

from pycsp3 import *

nWeeks, requirements, lb = data or load_json_data("05.json")

REST, MORN, DAY, EVE, JOKER = shifts = range(5)
nDays, nShifts, horizon = 7, len(shifts), 7 * nWeeks

# x[w][d] is the shift for day d in week w
x = VarArray(size=[nWeeks, nDays], dom=range(nShifts))

# z1 is the number of evenings before mornings
z1 = Var(dom=range(horizon + 1))

# z2 is the number of isolated rest days
z2 = Var(dom=range(horizon + 1))

# the objective to be minimized
z = Var(dom=range(lb, 2 * horizon + 1))

x_flat = flatten(x)  # useful auxiliary array for posting some constraints

satisfy(
    # ensuring shift requirements are satisfied
    [
        Count(
            within=x[:, d],
            value=s
        ) == requirements[s, d] for s in range(nShifts) for d in range(nDays)
    ],

    # ensuring that in any sequence of 7 days, at least one of them is a Rest day
    [
        Count(
            within=x_flat[i:i + 7],
            value=REST
        ) >= 1 for i in range(horizon)
    ],

    # ensuring there is no sequence of three Rest days in a row
    [
        Count(
            within=x_flat[i:i + 4],
            value=REST
        ) <= 3 for i in range(horizon)
    ],

    # counting Evenings before Mornings
    z1 == Sum(
        both(
            x_flat[i] == EVE,
            x_flat[i + 1] == MORN
        ) for i in range(horizon)
    ),

    # counting isolated Rest days
    z2 == Sum(
        conjunction(
            x_flat[i] != REST,
            x_flat[i + 1] == REST,
            x_flat[i + 2] != REST
        ) for i in range(horizon)
    ),

    # computing the objective value
    z == z1 + z2
)

minimize(
    z
)

"""
1) No need for x_flat_ext (longflatroster) because there is an auto-adjustment of array indexing
  x_flat_ext = x_flat + x_flat[:6]
"""
