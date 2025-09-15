"""
Travelling Salesperson Problem with Time Windows (TSPTW).

From Lewander's paper cited below: Consider 𝑛 locations that are to be visited, where there is a travelling duration between each directed
pair of locations and there is for each location u an earliest visiting time etu and a latest visiting time ltu.
A travelling salesperson tour with time windows (TSPTW ) of size 𝑛 is a Hamiltonian path of the weighted directed graph induced by the 𝑛 locations as nodes,
visiting each location u exactly once and between times etu and ltu.
The departure time at the last-visited location is to be minimised.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original mzn model was proposed by  Frej Knutar Lewander (MIT Licence assumed).

## Data Example
  n020w140-005.jso

## Model
  constraints: Circuit, Element

## Execution
  python TSPTW_z.py -data=<datafile.json>
  python TSPTW_z.py -data=<datafile.dzn> -parser=TSPTW_ParserZ.py

## Links
  - https://www.jair.org/index.php/jair/article/view/17482
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
"""

from pycsp3 import *

durations, early_times, late_times = data
nLocations = len(durations)

maxDuration = max(max(t) for t in durations)
minEarly = min(min(t) for t in early_times)
maxLate = max(max(t) for t in late_times)

depot = 0  # The first location is the depot

# pred[l] = the location visited before location l:
pred = VarArray(size=nLocations, dom=range(nLocations))

# durToPred[l] = the distance from location pred[l] to location l:
durToPred = VarArray(size=nLocations, dom=range(maxDuration + 1))

# arr[i] is the arrival time at the ith location
arr = VarArray(size=nLocations, dom=range(maxLate + 1))

# dep[i] is the departure time from the ith location
dep = VarArray(size=nLocations, dom=range(minEarly, maxLate + 1))

# departurePred[l] = the departure from location pred[l]:
departurePred = VarArray(size=nLocations, dom=range(maxLate + 1))

satisfy(
    [durToPred[i] == durations[i][pred[i]] for i in range(nLocations)],

    # starting at time 0 from the depot
    dep[depot] == 0,

    [dep[i] == max(arr[i], early_times[i]) for i in range(1, nLocations)],

    [departurePred[i] == dep[pred[i]] for i in range(nLocations)],

    # The arrival at location l is the departure from location pred[l] + The duration from pred[l] to l:
    [arr[i] == departurePred[i] + durToPred[i] for i in range(nLocations)],

    #  ensuring a circuit
    Circuit(pred, no_self_looping=True),

    # The departure from location l is before its latest visiting time late[l]:
    [dep[i] <= late_times[i] for i in range(nLocations)]
)

minimize(
    # minimizing the arrival time at depot
    arr[depot]
)
