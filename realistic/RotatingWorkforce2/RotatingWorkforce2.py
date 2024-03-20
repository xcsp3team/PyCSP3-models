"""
Rotating workforce scheduling problem.
See paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.

## Data Example
  e025s7.json

## Model
  constraints: Cardinality, Regular, Sum

## Execution
  python RotatingWorkforce2.py -data=<datafile.json>
  python RotatingWorkforce2.py -data=<datafile.dzn> -dataparser=RotatingWorkforce2_ParserZ.py

## Links
  - https://www.semanticscholar.org/paper/2-The-Rotating-Workforce-Scheduling-Problem-Musliu-Schutt/4048daa6fe7917009174dab7f3fe84e84fdc36dd
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
"""

from pycsp3 import *

nEmployees, requirements = data
nWeeks, nDays = nEmployees, 7

SATURDAY, SUNDAY = (5, 6)  # weekend
OFF, DAY, EVENING, NIGHT = Shifts = range(4)
nShifts = len(Shifts)
Not_off = range(1, nShifts)

q = Automaton.q

trs = [(q(0), Not_off, q(0)), (q(0), OFF, q(1)), (q(1), Not_off, q(0)), (q(1), OFF, q(2)), (q(2), Shifts, q(2))]
A1 = Automaton(start=q(0), final=q(2), transitions=trs)

trs = [(q(0), OFF, q(0)), (q(0), (DAY, EVENING), q(4)), (q(0), NIGHT, q(1))] \
      + [(q(1), OFF, q(0)), (q(1), NIGHT, q(2)), (q(2), OFF, q(0)), (q(2), NIGHT, q(3)), (q(3), OFF, q(0))] \
      + [(q(4), OFF, q(0)), (q(4), (DAY, EVENING), q(4))]
A2 = Automaton(start=q(0), final=[q(i) for i in range(5)], transitions=trs)

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

"""
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
