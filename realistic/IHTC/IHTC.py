"""
The Integrated Healthcare Timetabling Problem (IHTP), brings together three NP-hard problems and requires the following decisions:
  - (i) the admission date for each patient (or admission postponement to the next scheduling period),
  - (ii) the room for each admitted patient for the duration of their stay,
  - (iii) the nurse for each room during each shift of the scheduling period, and (iv) the operating theater (OT) for each admitted patient.
See ihtc2024.github.io

Important; the model proposed below (by C. Lecoutre) is an abridged version wrt the full problem.

## Data Example
  i01.json

## Model
  constraints: BinPacking, Cumulative, Element, Sum, Table

## Execution
  python IHTC.py -data=<datafile.json>
  python IHTC.py -data=<datafile.json> -parser=IHTC_Converter.py

## Links
  - https://ihtc2024.github.io/assets/files/ihtc2024_problem_specification.pdf
  - https://ihtc2024.github.io/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""
from pycsp3 import *

bp1, bp2 = False, True  # hard coding

nDays, nSkills, shifts, ages, occupants, patients, surgeons, theaters, rooms, nurses, weights = data or load_json_data("i01.json")

nShifts, nPatients, nSurgeons, nTheaters, nRooms, nNurses = nDays * 3, len(patients), len(surgeons), len(theaters), len(rooms), len(nurses)
assert shifts == ["early", "late", "night"]

GENDERS, A, B = ["A", "B"], 0, 1
assert all(patient.gender in GENDERS for patient in patients) and all(occupant.gender in GENDERS for occupant in occupants)
OCCUPANTS, PATIENTS, SURGEONS, THEATERS, ROOMS, NURSES = ALL = [[obj.id for obj in t] for t in (occupants, patients, surgeons, theaters, rooms, nurses)]
assert all(int(t[0][1:]) == 0 and all(int(t[i][1:]) + 1 == int(t[i + 1][1:]) for i in range(len(t) - 1)) for t in ALL)
DUMMY_DAY, DUMMY_ROOM, DUMMY_THEATER, DUMMY_NURSE = nDays, nRooms, nTheaters, nNurses
MAX = 100_000_000

max_stay = max(patient.length_of_stay for patient in patients)
shift_nurses = [[[i for i in range(nNurses) if any(asg.day == d and asg.shift == s for asg in nurses[i].working_shifts)] for s in shifts] for d in range(nDays)]
surgery_times = [sum(surgeon.max_surgery_time[d] for surgeon in surgeons) for d in range(nDays)]
sum_surgery_times = sum(surgery_times)
theater_times = [sum(theater.availability[d] for theater in theaters) for d in range(nDays)]
times = sorted([patient.surgery_duration for patient in patients])
nb_min_unscheduled = nPatients - number_max_of_values_for_sum_le(times, sum_surgery_times)
maxll = [number_max_of_values_for_sum_le(t, surgery_times[d]) for d in range(nDays)
         if (t := sorted(p.surgery_duration for p in patients if p.surgery_release_day <= d <= p.surgery_due_day and
                         surgeons[SURGEONS.index(p.surgeon_id)].max_surgery_time[d] >= p.surgery_duration),)]

P, D, R = range(nPatients), range(nDays), range(nRooms)

# pd[i] is the patient admission day of the ith patient
pd = VarArray(size=nPatients, dom=range(nDays + 1))  # +1 for DUMMY_DAY

# pr[i] is the patient admission room of the ith patient
pr = VarArray(size=nPatients, dom=range(nRooms + 1))  # +1 for DUMMY_ROOM

# pt[i] is the patient operating theater of the ith patient
pt = VarArray(size=nPatients, dom=range(nTheaters + 1))  # +1 for DUMMY_THEATER

# pl[i] is the effective stay length of the ith patient
pl = VarArray(size=nPatients, dom=lambda i: range(patients[i].length_of_stay + 1))

# pdt[i] is the admission day combined with the operating theater of the ith patient
ptd = VarArray(size=nPatients, dom=range((nDays + 1) * (nTheaters + 1)))

# nrs[d][s][r] is the nurse for the room r at shift s of day d
nrs = VarArray(size=[nDays, 3, nRooms], dom=lambda d, s, r: shift_nurses[d][s])  # introducing a dummy nurse?

# gender[d][r] is the gender of people in the rth room on the dth day
gender = VarArray(size=[nDays + max_stay, nRooms + 1], dom=lambda i, j: {A, B} if i < nDays and j < nRooms else {-1})

satisfy(
    [nrs[d][s][r] == shift_nurses[d][s][0] for d in D for s in range(3) for r in R],

    # respecting possible admission days of optional patients
    [pd[i] >= patients[i].surgery_release_day for i in P if not patients[i].mandatory],

    # respecting possible admission days of mandatory patients
    [pd[i] in range(patients[i].surgery_release_day, patients[i].surgery_due_day + 1) for i in P if patients[i].mandatory],

    # assigning patients to compatible rooms
    [pr[i].not_among(T) for i in P if (T := [int(s[1:]) for s in patients[i].incompatible_room_ids])],

    # computing ptd
    [ptd[i] == pd[i] * (nTheaters + 1) + pt[i] for i in P],

    # taking gender of occupants into account
    [gender[d][r] == g for occupant in occupants for d in range(occupant.length_of_stay)
     if (g := GENDERS.index(occupant.gender), r := ROOMS.index(occupant.room_id))],

    # ensuring no gender mix
    [
        If(
            pd[i] + k < DUMMY_DAY,
            Then=gender[pd[i] + k, pr[i]] == GENDERS.index(patients[i].gender)
        ) for i in P for k in range(patients[i].length_of_stay)
    ],

    # not exceeding daily working time of surgeons
    If(
        not bp1,
        Then=[
            Sum(patients[i].surgery_duration * (pd[i] == d) for i in P if patients[i].surgeon_id == surgeon.id) <= surgeon.max_surgery_time[d]
            for surgeon in surgeons for d in D
        ],
        Else=[
            BinPacking(
                partition=[pd[i] for i in SP],
                sizes=[patients[i].surgery_duration for i in SP],
                limits=surgeon.max_surgery_time + [MAX]
            ) for surgeon in surgeons if (SP := [i for i in P if patients[i].surgeon_id == surgeon.id],)
        ]),

    # not exceeding daily occupation time of theaters
    If(
        not bp2,
        Then=[
            Sum(patients[i].surgery_duration * both(pd[i] == d, pt[i] == k) for i in P) <= theaters[k].availability[d]
            for k, theater in enumerate(theaters) for d in D
        ],
        Else=BinPacking(
            partition=ptd,
            sizes=[patients[i].surgery_duration for i in P],
            limits=[0 if k == nTheaters else theaters[k].availability[d] for d in D for k in range(nTheaters + 1)] + [0] * nTheaters + [MAX])
    ),

    # handling postponed patients
    [(pd[i], pr[i], pt[i]) in {(DUMMY_DAY, DUMMY_ROOM, DUMMY_THEATER), (ne(DUMMY_DAY), ne(DUMMY_ROOM), ne(DUMMY_THEATER))} for i in P],

    # computing effective stay lengths
    [pl[i] == min(patients[i].length_of_stay, DUMMY_DAY - pd[i]) for i in P],

    # respecting room capacities
    [
        Cumulative(
            [
                Task(
                    origin=pd[i],
                    length=(pr[i] == r) * pl[i],
                    height=1
                ) for i in P
            ]
            +
            [
                Task(
                    origin=0,
                    length=occupant.length_of_stay,
                    height=1
                ) for i, occupant in enumerate(occupants) if occupant.room_id == rooms[r].id
            ]
        ) <= rooms[r].capacity for r in R
    ],

    # tag(redundant)
    [
        BinPacking(
            partition=pd,
            sizes=1,
            limits=maxll + [MAX]
        ),

        Sum(pd[i] == DUMMY_DAY for i in P) >= nb_min_unscheduled
    ]
)

minimize(
    weights.unscheduled_optional * Sum(pd[i] == DUMMY_DAY for i in P if not patients[i].mandatory)  # S8

    # Sum(
    #     # weights.open_operating_theater * NValues(ptd),  # , excepting=DUMMY_DAY * DUMMY_THEATER),  # S5
    #     # weights.surgeon_transfer * Sum(
    #     #     NValues([ptd[i] for i in range(nPatients) if patients[i].surgeon_id == surgeon.id], excepting=DUMMY_DAY * DUMMY_THEATER) for surgeon in surgeons),
    #     # # S6
    #     # weights.patient_delay * Sum(pd),  # S7
    #     weights.unscheduled_optional * Sum(pd[i] == DUMMY_DAY for i, patient in enumerate(patients) if not patient.mandatory)  # S8
    # ) - weights.patient_delay * sum(patient.surgery_release_day for patient in patients) - weights.open_operating_theater,  # we assume at least one DUMMY
)

# - weights.patient_delay * sum(patient.surgery_release_day for patient in patients),  # S7

"""
TODO : somme des surgery times et compter le nb min de dummy days (et temps des theaters ?)
       compter nombre de places par jour (changeable avec les occupants) et indiquer le nb d'opertaions par jour possible
       gender calculer le nb min de romms d'un genre et d'un autre (attention on peut pousser A au debut et B a la fin) donc pas evident
1) S7 : what about the non scheduled patients ? discard them ?
2) if only one theater one can simplify
3) think about no gender mix (-1 necessary ?)
"""

#  weights.patient_delay * Sum(pd[i] - patient.surgery_release_day for i, patient in enumerate(patients)),  # S7

# for p1, p2 in combinations(patients, 2):
#     if all(getattr(p1, name) == getattr(p2, name) for name in p1._fields if name != "id"):
#         print(p1, p2)


# [
#     Table(
#         scope=pr[i],
#         conflicts=[int(s[1:]) for s in patients[i].incompatible_room_ids]
#     ) for i, patient in enumerate(patients)
# ],
