"""
This problem is taken from real life rostering challenges (like nurse rostering).
The task is it to find a shift assignment for every employee for every day.
A rotation system is used to decrease the size of the problem.
Thus, only the rostering for one employee is calculated and all other employees gain a rotated version of the rostering.
So Employee 2 has in the first week the rostering of Employee 1 in the second week.
Employee 3 has in the first week the rostering of Employee 2 in the second week and Employee 1 in the third week etc.

See problem 087 at CSPLib.

## Data
  008-2-3.json

## Model
  constraints: AllEqual, Cardinality, Count, Table

## Execution
  python RotatingRostering.py -data=<datafile.json>
  python RotatingRostering.py -data=<datafile.txt> -parser=RotatingRostering_ParserE.py

## Links
  - https://www.csplib.org/Problems/prob087/

## Tags
  realistic, csplib, xcsp25
"""

from pycsp3 import *

nDaysPerWeek, nWeeks, shift_min, shift_max, requirements = data
nDays = nWeeks * nDaysPerWeek

SATURDAY, SUNDAY = 5, 6
shifts = (OFF, EARLY, LATE, NIGHT) = range(4)
nShifts = len(shifts)

# x[i] is the shift for the ith day (along the flattened horizon)
x = VarArray(size=nDays, dom=range(nShifts))

# y[w][d] is the shift in the dth day of the wth week
y = VarArray(size=[nWeeks, nDaysPerWeek], dom=range(nShifts))

satisfy(
    # computing y
    [y[w][d] == x[w * nDaysPerWeek + d] for w in range(nWeeks) for d in range(nDaysPerWeek)],

    # ensuring weekend days (Saturday and Sunday) have the same shift
    [y[w][SATURDAY] == y[w][SUNDAY] for w in range(nWeeks)],

    # ensuring a minimum length of consecutive similar shifts
    [
        If(
            x[i] != x[i + 1],
            Then=AllEqual(x[i + 1:i + 1 + shift_min])
        ) for i in range(nDays)
    ],

    # ensuring a maximum length of consecutive similar shifts
    [
        If(
            AllEqual(x[i:i + shift_max]),
            Then=x[i] != x[i + shift_max]
        ) for i in range(nDays)
    ],

    # ensuring to have at least 2 resting days every 2 weeks
    [
        Count(
            within=x[i:i + 2 * nDaysPerWeek + 1],
            value=OFF
        ) >= 2 for i in range(nDays)  # does seem to be +1 in the model posted at CSPLib?
    ],

    # avoiding some specific successive shifts
    [(x[i], x[i + 1]) not in {(LATE, EARLY), (NIGHT, EARLY), (NIGHT, LATE)} for i in range(nDays)],

    # ensuring the right number of employees
    [
        Cardinality(
            within=y[:, d],
            occurrences={s: requirements[d][s] for s in range(nShifts)}
        ) for d in range(nDaysPerWeek)
    ]

)

test = False
if test:
    gap = 144
    nWeeks += gap
    requirements = [[v + gap // 4 for v in t] for t in requirements]

# # restricts the order of shifts. $ There is a forward rotating principle. This means, that after an early shift there can only follow a shift with the same or a higher value, or a rest shift.
# [
#     [either(plan1d[day + 1] == 0, plan1d[day] <= plan1d[day + 1]) for day in range(1, nDays - 1)],
#
#     # forward rotating
#     either(plan1d[0] == 0, plan1d[0] >= plan1d[-1]),
# ],

# [Sum(plan1d[i] == 0 for i in range(day, day + nDaysPerWeek * 2)) >= 2 for day in range((nWeeks - 2) * nDaysPerWeek)],
#
#     [Sum(plan1d[j] == 0 for j in range(nDays - i, nDays)) + Sum(plan1d[k] == 0 for k in range(2 * nDaysPerWeek - i)) >= 2
#      for i in range(2 * nDaysPerWeek - 1)],

# # for every shift type a maximum number of consecutive assignments to this shift is given
# [
#     If(
#         [plan1d[d] == plan1d[i] for i in range(d + 1, d + shift_max)],
#         Then=plan1d[d] != plan1d[d + shift_max]
#
#     ) for d in range(nDays - shift_max)
# ],
#
# # the constraints over the array bounds
# [
#     If(
#         [s_maxarr[d, 0] == s_maxarr[d, i] for i in range(1, shift_max)],
#         Then=plan1d[d + nDays - shift_max] != plan1d[d]
#
#     ) for d in range(shift_max)
# ],

# # or every shift type a minimum number of consecutive assignments to this shift is given
# [
#     If(
#         plan1d[day] != plan1d[day + 1],
#         Then=[plan1d[i] == plan1d[i + 1] for i in range(day + 1, day + shift_min)]
#     ) for day in range(nDays - shift_min)
# ],
#
# #  the constraints over the array bounds
# [
#     If(
#         plan1d[d + nDays - shift_min] != plan1d[((d + nDays - shift_min) % nDays)],
#         Then=[s_minarr[d, 0] == s_minarr[d, i] for i in range(1, shift_min)]
#     ) for d in range(shift_min)
#
# ],


# s_minarr = VarArray(size=[shift_min, shift_min], dom=range(nShifts))

# s_maxarr = VarArray(size=[shift_max, shift_max], dom=range(nShifts))

# create the sub arrays over the array bounds
# [s_minarr[i, j] == plan1d[(nDays - shift_min + 1 + i + j) % nDays] for i in range(shift_min) for j in range(shift_min)],

# create the sub arrays other the array bounds
# [s_maxarr[i, j] == plan1d[((nDays - shift_max + i + j) % nDays)] for i in range(shift_max) for j in range(shift_max)],
