"""
Realistic employee shift scheduling Problem.

## Data Example
  00.json

## Model
  constraints: Count, Regular, Sum, Table

## Execution
  python NurseRostering.py -data=<datafile.json>

## Links
  - http://www.schedulingbenchmarks.org/nurseinstances1_24.html
  - https://link.springer.com/chapter/10.1007/978-3-642-04244-7_9
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
"""

from pycsp3 import *

nDays, shifts, staff, covers = data or load_json_data("00.json")

if shifts[-1].id != "_off":  # if not present, we add first a dummy 'off' shift (a named tuple of the right class)
    shifts.append(shifts[0].__class__("_off", 0, None))
OFF = len(shifts) - 1  # value for _off
lengths = [shift.length for shift in shifts]

nWeeks, nShifts, nPersons = nDays // 7, len(shifts), len(staff)
D, P, S, W = range(nDays), range(nPersons), range(nShifts), range(nWeeks)

on_r = [[next((r for r in staff[p].onRequests if r.day == d), None) if staff[p].onRequests else None for d in D] for p in P]
off_r = [[next((r for r in staff[p].offRequests if r.day == d), None) if staff[p].offRequests else None for d in D] for p in P]

# kmin for minConsecutiveShifts, kmax for maxConsecutiveShifts, kday for minConsecutiveDaysOff
_, maxShifts, minTimes, maxTimes, kmin, kmax, kday, maxWeekends, daysOff, _, _ = zip(*staff)

sp = {shifts[s].id: s for s in S}  # position of shifts in the list 'shifts'
T = {(sp[shift1.id], sp[shift2]) for shift1 in shifts if shift1.forbiddenFollowingShifts for shift2 in shift1.forbiddenFollowingShifts}  # rotation


def costs(day, shift):
    if shift == OFF:
        return [0] * (nPersons + 1)
    r, wu, wo = covers[day][shift]
    return [abs(r - p) * (wu if p <= r else wo) for p in range(nPersons + 1)]


def build_automaton(k, for_shifts):  # automaton_min_consecutive
    q = Automaton.q  # for building state names
    r1, r2 = (OFF, S[:-1]) if for_shifts else (S[:-1], OFF)  # S[:-1] a range with all values other than OFF
    t = [(q(0), r1, q(1)), (q(0), r2, q(k + 1)), (q(1), r1, q(k + 1))] + [(q(i), r2, q(i + 1)) for i in range(1, k + 1)] + [(q(k + 1), S, q(k + 1))]
    return Automaton(start=q(0), final=q(k + 1), transitions=t)


# x[d][p] is the shift at day d for person p (value 'OFF' denotes off)
x = VarArray(size=[nDays, nPersons], dom=range(nShifts))

# nd[p][s] is the number of days such that person p works with shift s
nd = VarArray(size=[nPersons, nShifts], dom=lambda p, s: range((nDays if s == OFF else maxShifts[p][s]) + 1))

# np[d][s] is the number of persons working on day d with shift s
np = VarArray(size=[nDays, nShifts], dom=range(nPersons + 1))

# wk[p][w] is 1 iff the weekend w is worked by person p
wk = VarArray(size=[nPersons, nWeeks], dom={0, 1})

# cn[p][d] is the cost of not satisfying the on-request (if it exists) of person p on day d
cn = VarArray(size=[nPersons, nDays], dom=lambda p, d: {0, on_r[p][d].weight} if on_r[p][d] else None)

# cf[p][d] is the cost of not satisfying the off-request (if it exists) of person p on day d
cf = VarArray(size=[nPersons, nDays], dom=lambda p, d: {0, off_r[p][d].weight} if off_r[p][d] else None)

# cc[d][s] is the cost of not satisfying cover for shift s on day d
cc = VarArray(size=[nDays, nShifts], dom=lambda d, s: costs(d, s))

satisfy(
    # days off for staff
    [x[d][p] == OFF for d in D for p in P if d in daysOff[p]],

    # computing number of days
    [Count(within=x[:, p], value=s) == nd[p][s] for p in P for s in S],

    # computing number of persons
    [Count(within=x[d], value=s) == np[d][s] for d in D for s in S],

    # computing worked weekends
    [
        (
            If(x[w * 7 + 5][p] != OFF, Then=wk[p][w]),
            If(x[w * 7 + 6][p] != OFF, Then=wk[p][w])
        ) for p in P for w in W
    ],

    # rotation shifts
    [Slide((x[d][p], x[d + 1][p]) not in T for d in D[:-1]) for p in P] if len(T) > 0 else None,

    # maximum number of worked weekends
    [Sum(wk[p]) <= maxWeekends[p] for p in P],

    # minimum and maximum number of total worked minutes
    [nd[p] * lengths in range(minTimes[p], maxTimes[p] + 1) for p in P],

    # maximum consecutive worked shifts
    [Count(within=x[d:d + kmax[p] + 1, p], value=OFF) >= 1 for p in P for d in range(nDays - kmax[p])],

    # minimum consecutive worked shifts
    [
        Regular(
            scope=x[d: d + kmin[p] + 1, p],
            automaton=build_automaton(kmin[p], True)
        ) for p in P for d in range(nDays - kmin[p])
    ],

    # managing off days on schedule ends
    [
        (
            If(x[0][p] != OFF, Then=x[d][p] != OFF),
            If(x[-1][p] != OFF, Then=x[-1 - d][p] != OFF)
        ) for p in P if kmin[p] > 1 for d in range(1, kmin[p])
    ],

    # minimum consecutive days off
    [
        Regular(
            scope=x[d: d + kday[p] + 1, p],
            automaton=build_automaton(kday[p], False)
        ) for p in P for d in range(nDays - kday[p])
    ],

    # cost of not satisfying on requests
    [(x[d][p] == sp[on_r[p][d].shift]) == (cn[p][d] == 0) for p in P for d in D if on_r[p][d]],

    # cost of not satisfying off requests
    [(x[d][p] == sp[off_r[p][d].shift]) == (cf[p][d] != 0) for p in P for d in D if off_r[p][d]],

    # cost of under or over covering
    [
        Table(
            scope=(np[d][s], cc[d][s]),
            supports=[(i, v) for i, v in enumerate(costs(d, s))]
        ) for d in D for s in S
    ]
)

minimize(
    Sum(cn) + Sum(cf) + Sum(cc)
)

""" Comments
1) Note that we could have written:
 [iff(x[d][p] == s, cn[p][d] == 0) for (p,d,s) in [(p,d, sp[on_r[p][d].shift]) for p in P for d in D if on_r[p][d]]],
"""

# [Cardinality(x[:, p], occurrences=nd[p]) for p in P],
# [Cardinality(x[d], occurrences=np[d]) for d in D],
