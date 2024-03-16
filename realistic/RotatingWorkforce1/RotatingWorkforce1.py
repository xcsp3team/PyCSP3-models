"""
Rotating Workforce Scheduling.

The problem aims to schedule workers satisfying shift sequence constraints while ensuring that enough shifts are covered on each day.
All workers complete the same schedule, just starting at different days.
See CPAIOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2019 Minizinc challenges.
The MZN model was proposed by Andreas Schutt.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  0103.json

## Model
  constraints: Cardinality, Regular

## Execution
  python RotatingWorkforce1.py -data=<datafile.json>
  python RotatingWorkforce1.py -data=<datafile.dzn> -parser=RotatingWorkforce1_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-93031-2_31
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn18, mzn19
"""

from pycsp3 import *
from pycsp3.problems.data.parsing import split_with_rows_of_size

weekLength, nWorkers, daysOff, workBlockLength, needs, shifts, forbids = data
assert daysOff.min <= 2 and sum(needs[:, -1]) < nWorkers
nShifts, nDays = len(shifts), weekLength

OFF = nShifts
nOnDutyDays = sum(sum(needs[j]) for j in range(nShifts))
nOffDutyDays = weekLength * nWorkers - nOnDutyDays

S, Sp1, D, W = range(nShifts), range(nShifts + 1), range(nDays), range(nWorkers)


def automaton():
    def state(shift, day, dayw):
        return first[shift] + (workBlockLength.max * (day - 1)) + (dayw - 1)

    OFF2 = nShifts + 2  # The state of the DFA when the current block is an off-duty one and at least of length two
    first = [1 + nShifts + daysOff.max + sum(workBlockLength.max * shifts[j].blockMax for j in range(i)) for i in S]
    toff = [[(not any(before == i and after == j for (before, after, doff) in forbids if doff == 1)) for j in S] for i in S]
    ton = [[(not any(before == i and after == j for (before, after, doff) in forbids if doff == 0)) for j in S] for i in S]

    t = first + [OFF2]
    t += [(OFF2 if 1 < daysOff.max else 0) if j == OFF else first[j] if 1 >= daysOff.min and toff[i][j] else 0 for i in S for j in Sp1]
    t += [(nShifts + 1 + d if d < daysOff.max else 0) if j == OFF else first[j] if d >= daysOff.min else 0 for d in range(2, daysOff.max + 1) for j in Sp1]

    def val(i, shift, ds, dw, j):
        if j == OFF:
            return i + 1 if ds >= shift.blockMin and dw >= workBlockLength.min else 0
        if j == i:
            return state(i, ds + 1, dw + 1) if ds < shift.blockMax and dw < workBlockLength.max else 0
        return state(j, 1, dw + 1) if ds >= shift.blockMin and dw < workBlockLength.max and ton[i][j] else 0

    t += [val(i, shift, ds, dw, j) for i, shift in enumerate(shifts) for ds in range(1, shift.blockMax + 1) for dw in range(1, workBlockLength.max + 1)
          for j in Sp1]

    t = split_with_rows_of_size(t, nShifts + 1)
    q = Automaton.q
    trs = [(q(i + 1), j, q(t[i][j])) for i in range(len(t)) for j in Sp1 if t[i][j] != 0]
    return Automaton(start=q(1), final=[q(i) for i in range(1, len(t) + 1)], transitions=trs)


# x[i][d] is the shift for the ith worker on the dth day
x = VarArray(size=[nWorkers + 1, nDays], dom=range(nShifts + 1))

satisfy(
    # linking the first worker/week to the additional one at the end
    x[0] == x[-1],

    # ensuring requirements of shifts are met
    [
        Cardinality(
            x[:-1, d],
            occurrences={j: needs[j][d] for j in S} | {OFF: nWorkers - sum(needs[:, d])}  # needs Python 3.9
        ) for d in D
    ],

    # ensuring legal rules are respected
    x in automaton(),

    # tag(symmetry-breaking)
    (
        x[-2][-1] == OFF if sum(needs[:, -1]) < nWorkers else None,

        x[0][0] != OFF if all(needs[j][d] == needs[j][d + 1] for j in S for d in range(nDays - 1)) or sum(needs[:, -1]) < sum(needs[:, 0]) else None
    )
)


def post_redundant_constraints():
    # number of off-duty days from first day until the end of the week
    count_off_duty = VarArray(size=nWorkers, dom=range(nOffDutyDays + 1))

    # number of off-duty days after the end of the week
    rem_off = VarArray(size=nWorkers, dom=range(nOffDutyDays + 1))

    # number of on-duty days after the end of the week
    rem_on = VarArray(size=nWorkers, dom=range(nOnDutyDays + 1))

    # lower bound of off-duty blocks
    lb_off_blocks = VarArray(size=nWorkers, dom=range(-1, nOffDutyDays // daysOff.max + 2))

    # upper bound of on-duty blocks
    ub_on_blocks = VarArray(size=nWorkers, dom=range(nOnDutyDays // workBlockLength.min + 2))

    # lower bound of on-duty blocks
    lb_on_blocks = VarArray(size=nWorkers, dom=range(-1, nOnDutyDays // workBlockLength.max + 2))

    # upper bound of off-duty blocks
    ub_off_blocks = VarArray(size=nWorkers, dom=range(nOffDutyDays // daysOff.min + 2))

    satisfy(
        # counting the number of off-duty days after the end of the week
        [rem_off[i] == nOffDutyDays - count_off_duty[i] for i in W],

        # counting the number of on-duty days after the end of the week
        [rem_on[i] == nOnDutyDays - weekLength * (i + 1) + count_off_duty[i] for i in W],

        # lower bound of off-duty blocks
        [lb_off_blocks[i] == (rem_off[i] // daysOff.max) + (rem_off[i] % daysOff.max > 0) - ((x[0][0] != OFF) & (x[i + 1][0] == OFF)) for i in W],

        # upper bound of on-duty blocks
        [ub_on_blocks[i] == (rem_on[i] // workBlockLength.min) + ((x[0][0] != OFF) & (x[i][-1] != OFF)) for i in W],

        # lower bound of on-duty blocks
        [lb_on_blocks[i] == (rem_on[i] // workBlockLength.max) + (rem_on[i] % workBlockLength.max > 0) - ((x[0][0] == OFF) & (x[i + 1][0] != OFF)) for i in W],

        # upper bound of off-duty blocks
        [ub_off_blocks[i] == (rem_off[i] // daysOff.min) + ((x[0][0] == OFF) & (x[i][-1] == OFF)) for i in W],

        # the first week is just the sum of the off-duty days in that week
        count_off_duty[0] == Sum(x[0][d] == OFF for d in D),

        # the remaining weeks are the sum of the previous weeks and the current one
        [count_off_duty[i] == count_off_duty[i - 1] + Sum(x[i][d] == OFF for d in D) for i in range(1, nWorkers)],

        # the sum of the last week must be equal to the number of off-duty days
        count_off_duty[-1] == nOffDutyDays,

        # the lower bound on the remaining off-duty blocks must be not greater than the upper bound on the remaining on-duty blocks
        [lb_off_blocks[i] <= ub_on_blocks[i] for i in W],

        # the lower bound on the remaining on-duty blocks must be not greater than the upper bound on the remaining off-duty blocks
        [lb_on_blocks[i] <= ub_off_blocks[i] for i in W]
    )


post_redundant_constraints()

"""
1) this solution from MZN (chuffed) for 1479 is ok:
   flatten(x) == decrement(
        [1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2,
         4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1,
         2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1,
         1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 2, 2, 4, 4, 1, 1, 1, 1, 1, 4, 4, 4,
         1, 1, 1, 1, 1, 4, 4, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 1, 1, 1, 3, 3, 3, 4, 4, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 3,
         3, 3, 3, 4, 4, 4, 1, 1, 1, 3, 3, 3, 4, 4, 1, 1, 1, 3, 3, 3, 4, 4, 3, 3, 3, 3, 4, 4, 2, 2, 2, 3, 3, 3, 4, 4, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1,
         1, 2, 2, 4]),
2) need python 3.9 (for handling the union of dictionaries)
"""
