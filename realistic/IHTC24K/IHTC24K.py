"""
The Integrated Healthcare Timetabling Problem (IHTP), brings together three NP-hard problems and requires the following decisions:
  - (i) the admission date for each patient (or admission postponement to the next scheduling period),
  - (ii) the room for each admitted patient for the duration of their stay,
  - (iii) the nurse for each room during each shift of the scheduling period, and (iv) the operating theater (OT) for each admitted patient.
See ihtc2024.github.io

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
The original mzn model by  Lucas Kletzander -- No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  i02.json

## Model
  constraints: Count, Cumulative, Element, Sum

## Execution
  python IHTC24K.py -data=<datafile.json>
  python IHTC24K.py -data=<datafile.json> -parser=IHTC24K_ParserZ.py

## Links
  - https://ihtc2024.github.io/assets/files/ihtc2024_problem_specification.pdf
  - https://ihtc2024.github.io/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
"""

from pycsp3 import *

occupants, patients, max_surgery, room_capacities, max_ot, weight_selection, weight_delay = data
oc_length_of_stay, oc_gender, oc_room = occupants
length_of_stay, gender, incompatible_rooms, mandatory, surgery_duration, surgeon, release_day, due_day = patients

nOccupants, nPatients, nSurgeons, nRooms, nTheaters, horizon = len(oc_gender), len(gender), len(max_surgery), len(room_capacities), len(max_ot), len(
    max_ot[0])

selection = VarArray(size=nPatients, dom={0, 1})

# pd[i] is the patient admission day of the ith patient
pd = VarArray(size=nPatients, dom=range(horizon))

# pr[i] is the patient admission room of the ith patient
pr = VarArray(size=nPatients, dom=range(nRooms))

# pt[i] is the patient operating theater of the ith patient
pt = VarArray(size=nPatients, dom=range(nTheaters))

room_admission = VarArray(size=[nRooms, nPatients], dom=range(max(length_of_stay) * nPatients + 1))

satisfy(
    # H1 No gender mix
    [
        If(
            selection[p],
            Then=either(oc_room[c] != pr[p], pd[p] >= oc_length_of_stay[c])
        ) for c in range(nOccupants) for p in range(nPatients) if oc_gender[c] != gender[p]
    ],

    [
        If(
            selection[p1], selection[p2],
            Then=disjunction(pr[p1] != pr[p2], pd[p1] >= pd[p2] + length_of_stay[p2], pd[p2] >= pd[p1] + length_of_stay[p1])
        ) for p1 in range(nPatients) for p2 in range(nPatients) if gender[p1] != gender[p2]
    ],

    #  H2 Compatible rooms
    [pr[p] not in incompatible_rooms[p] for p in range(nPatients)],

    #  H3 Surgeon overtime
    [Sum(surgery_duration[p] * selection[p] * (pd[p] == d) * (surgeon[p] == s) for p in range(nPatients)) <= max_surgery[s, d]
     for s in range(nSurgeons) for d in range(horizon)],

    # H4 OT overtime
    [Sum(surgery_duration[p] * selection[p] * (pd[p] == d) * (pt[p] == o) for p in range(nPatients)) <= max_ot[o, d]
     for o in range(nTheaters) for d in range(horizon)],

    # H5 Mandatory patients
    [selection[p] == 1 for p in range(nPatients) if mandatory[p]],

    # H6 Admission day
    [pd[p] in range(release_day[p], due_day[p] + 1) for p in range(nPatients)],

    # H7 Room capacity
    [
        If(
            selection[p],
            Then=room_admission[pr[p], p] == pd[p]
        ) for p in range(nPatients)
    ],

    [
        Cumulative(
            origins=[0] * len(C) + room_admission[r],
            lengths=oc_length_of_stay[C] + length_of_stay,
            heights=1
        ) <= room_capacities[r] for r in range(nRooms) if (C := [c for c in range(nOccupants) if oc_room[c] == r],)
    ]
)

minimize(
    Count(selection, value=0) * weight_selection
    + Sum(selection[p] * (pd[p] - release_day[p]) for p in range(nPatients)) * weight_delay
)
