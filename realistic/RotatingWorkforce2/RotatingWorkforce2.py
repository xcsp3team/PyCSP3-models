"""
Rotating workforce scheduling problem.
See paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.

## Data Example
  e025s7.json

## Model
  constraints: Cardinality, Regular, Sum

## Execution
  python RotatingWorkforce2.py -data=<datafile.json>
  python RotatingWorkforce2.py -parser=RotatingWorkforce_Random.py <number> <number>
  python RotatingWorkforce2.py -data=<datafile.dzn> -parser=RotatingWorkforce2_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-93031-2_31
  - https://www.minizinc.org/challenge/2022/results/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  realistic, mzn22, xcsp24
"""

from pycsp3 import *

nEmployees, requirements = data
nWeeks, nDays = nEmployees, 7

SATURDAY, SUNDAY = (5, 6)  # weekend
OFF, DAY, EVENING, NIGHT = Shifts = range(4)
nShifts = len(Shifts)
NOT_OFF = range(1, nShifts)

q0, q1, q2, q3, q4 = states = Automaton.states_for(range(5))

A1 = Automaton(start=q0, final=q2, transitions=[(q0, NOT_OFF, q0), (q0, OFF, q1), (q1, NOT_OFF, q0), (q1, OFF, q2), (q2, Shifts, q2)])

A2 = Automaton(start=q0, final=states, transitions=[(q0, OFF, q0), (q0, (DAY, EVENING), q4), (q0, NIGHT, q1), (q1, OFF, q0), (q1, NIGHT, q2), (q2, OFF, q0),
                                                    (q2, NIGHT, q3), (q3, OFF, q0), (q4, OFF, q0), (q4, (DAY, EVENING), q4)])

# x[i][j] is the shift for the jth day of the ith week
x = VarArray(size=[nWeeks, nDays], dom=range(nShifts))

# fw[i] is 1 if the weekend of the ith week is free
fw = VarArray(size=nWeeks, dom={0, 1})

x_flat = flatten(x)

satisfy(
    # ensuring shift requirements are met for each day
    [
        Cardinality(
            within=x[:, j],
            occurrences={i: requirements[j][i - 1] for i in range(1, nShifts)}
        ) for j in range(nDays)
    ],

    # at least 2 consecutive days off each week
    [x[i] in A1 for i in range(nWeeks)],

    # at most five days without rest
    [
        Sum(
            x_flat[j] == 0 for j in range(i, i + 6)
        ) != 0 for i in range(0, nWeeks * nDays)
    ],

    # computing free weekends
    [
        fw[i] == both(
            x[i][SATURDAY] == 0,
            x[i][SUNDAY] == 0
        ) for i in range(nWeeks)
    ],

    # at least 1 out of 3 weekends off
    [Exist(fw[i:i + 3], value=1) for i in range(nWeeks)],

    # at most 3 night-shifts in a row, and then rest
    x[:nWeeks + 2] in A2
)

""" Comments
1) Note that index auto-adjustment is used, meaning that
   Sum(fw[j]) == 1
 is equivalent to:
   Sum(fw[j % nWeeks]) == 1
2) Note that:
  x[:nWeeks + 2] 
is equivalent to:
  x[i % nWeeks] for i in range(nWeeks + 2)] 
3) Minizinc solution (chuffed) for instance 030; testing it with the constraint:
 flatten(x) == [3, 3, 3, 0, 0, 3, 3, 3, 0, 3, 3, 0, 0, 3, 3, 3, 0, 3, 3, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 3, 0, 3, 0, 0, 3, 3, 0, 3, 3, 0, 0, 0, 1, 1, 1, 1, 0,
    0, 3, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0,
    1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 1, 0, 2, 1, 1, 1, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 0, 2, 2, 2,
    2, 0, 2, 2, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2, 2, 0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0,
    0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0],
"""

# xp = [x[i % nWeeks] for i in range(nWeeks + 2)]  # x cyclicly extended to the two first weeks
