"""
Balanced Nursing Workload Problem.
See Problem 069 at CSPLib.

## Data Example
  2zones1.json

## Model
  constraints: Cardinality, Sum

## Execution
  python NursingWorkload.py -data=<datafile.json>
  python NursingWorkload.py -data=<datafile.txt> -parser=NursingWorkload_Parser.py

## Links
  - https://www.csplib.org/Problems/prob069/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
"""

from pycsp3 import *

nNurses, minPatientsPerNurse, maxPatientsPerNurse, maxWorkloadPerNurse, demands = data
patients = [(i, demand) for i, t in enumerate(demands) for demand in t]
nPatients, nZones = len(patients), len(demands)

lb = sum(sorted(demand for i, t in enumerate(demands) for demand in t)[:minPatientsPerNurse])

# p[i] is the nurse assigned to the ith patient
p = VarArray(size=nPatients, dom=range(nNurses))

# w[k] is the workload of the kth nurse
w = VarArray(size=nNurses, dom=range(lb, maxWorkloadPerNurse + 1))

satisfy(
    # ensuring that each nurse has a valid number of patients
    Cardinality(
        within=p,
        occurrences={k: range(minPatientsPerNurse, maxPatientsPerNurse + 1) for k in range(nNurses)}
    ),

    # ensuring a nurse stays within a zone
    [p[i] != p[j] for i, j in combinations(nPatients, 2) if patients[i][0] != patients[j][0]],

    # computing the workload of each nurse
    [
        w[k] == Sum(
            c * (p[i] == k) for i, (_, c) in enumerate(patients)
        ) for k in range(nNurses)
    ],

    # tag(symmetry-breaking)
    [p[z] == z for z in range(nZones)],

    Increasing(w)
)

minimize(
    w * w
)

""" Comments
1) Note that:
 w * w
   is equivalent to:
 Sum(w[k] * w[k] for k in range(nNurses))
2) is Increasing(w), a kind of symmetry-breaking compatible with the group just above?
"""
