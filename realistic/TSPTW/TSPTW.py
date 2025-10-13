"""
Travelling Salesperson Problem with Time Windows (TSPTW).

From Lewander's paper cited below: Consider 𝑛 locations that are to be visited, where there is a travelling duration between each directed
pair of locations and there is for each location u an earliest visiting time etu and a latest visiting time ltu.
A travelling salesperson tour with time windows (TSPTW ) of size 𝑛 is a Hamiltonian path of the weighted directed graph induced by the 𝑛 locations as nodes,
visiting each location u exactly once and between times etu and ltu.
The departure time at the last-visited location is to be minimised.

This model is a simplified (but equivalent) version of TSPTW_z (submitted to the 2025 Minizinc challenge).

## Data Example
  n020w140-005.json

## Model
  constraints: Circuit, Element

## Execution
  python TSPTW.py -data=<datafile.json>
  python TSPTW.py -data=<datafile.dzn> -parser=TSPTW_ParserZ.py

## Links
  - https://www.jair.org/index.php/jair/article/view/17482
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic
"""

from pycsp3 import *

durations, early_times, late_times = data or load_json_data("n020w140-005.json")

nLocations = len(durations)

DEPOT = 0  # The first location is the depot

# pred[i] is the location visited just before the ith location
pred = VarArray(size=nLocations, dom=range(nLocations))

# arr[i] is the arrival time at the ith location
arr = VarArray(size=nLocations, dom=lambda i: range(late_times[i] + 1))

# dep[i] is the departure time from the ith location
dep = VarArray(size=nLocations, dom=lambda i: range(early_times[i], late_times[i] + 1))

satisfy(
    # ensuring a circuit
    Circuit(pred, no_self_looping=True),

    # starting at time 0 from the depot
    dep[DEPOT] == 0,

    # leaving after arriving
    [dep[i] >= arr[i] for i in range(1, nLocations)],

    # computing arrival times
    [arr[i] == dep[pred[i]] + durations[i][pred[i]] for i in range(nLocations)]
)

minimize(
    # minimizing the arrival time at depot
    arr[DEPOT]
)
