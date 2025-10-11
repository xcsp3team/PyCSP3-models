"""
Rotating workforce scheduling problem.

From the CPAIOR paper cited below: Rotating workforce scheduling is a specific personnel scheduling problem arising in many spheres of life such as, e.g., industrial plants, hospitals,
public institutions, and airline companies. A schedule must meet many constraints such as workforce requirements for shifts and days, minimal
and maximal length of shifts, and shift transition constraints.

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

nEmployees, requirements = data or load_json_data("e025s7.json")

SATURDAY, SUNDAY = (5, 6)  # weekend
OFF, DAY, EVENING, NIGHT = Shifts = range(4)
nShifts = len(Shifts)
NOT_OFF = range(1, nShifts)

nWeeks, nDays = nEmployees, 7
W, D = range(nWeeks), range(nDays)


def build_automaton1():
    q0, q1, q2 = Automaton.states_for(range(3))
    return Automaton(start=q0, final=q2, transitions=[(q0, NOT_OFF, q0), (q0, OFF, q1), (q1, NOT_OFF, q0), (q1, OFF, q2), (q2, Shifts, q2)])


def build_automaton2():
    q0, q1, q2, q3, q4 = states = Automaton.states_for(range(5))
    trs = [(q0, OFF, q0), (q0, (DAY, EVENING), q4), (q0, NIGHT, q1), (q1, OFF, q0), (q1, NIGHT, q2), (q2, OFF, q0), (q2, NIGHT, q3), (q3, OFF, q0),
           (q4, OFF, q0), (q4, (DAY, EVENING), q4)]
    return Automaton(start=q0, final=states, transitions=trs)


# x[i][j] is the shift for the jth day of the ith week
x = VarArray(size=[nWeeks, nDays], dom=range(nShifts))

# fw[i] is 1 if the weekend of the ith week is free
fw = VarArray(size=nWeeks, dom={0, 1})

satisfy(
    # ensuring shift requirements are met for each day
    [
        Cardinality(
            within=x[:, j],
            occurrences={i: requirements[j][i - 1] for i in range(1, nShifts)}
        ) for j in D
    ],

    # at least 2 consecutive days off each week
    [
        Regular(
            scope=x[i],
            automaton=build_automaton1()
        ) for i in W
    ],

    # at most five days without rest
    [Sum(x[j // nDays][j % nDays] == OFF for j in range(i, i + 6)) > 0 for i in range(0, nWeeks * nDays)],

    # computing free weekends
    [
        fw[i] == both(
            x[i][SATURDAY] == OFF,
            x[i][SUNDAY] == OFF
        ) for i in W
    ],

    # at least 1 out of 3 weekends off
    [
        Exist(
            within=fw[i:i + 3],
            value=1
        ) for i in W
    ],

    # at most 3 night-shifts in a row, and then rest
    Regular(
        scope=x[:nWeeks + 2],
        automaton=build_automaton2()
    )
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
3) Note that
    Sum(x[j // nDays][j % nDays] == OFF
  could be written:
     Sum(x_flat[j] == OFF
  after having defined:
     x_flat = flatten(x)
"""
